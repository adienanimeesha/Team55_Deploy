import json
import re
from urllib.parse import urlencode
from django.db.models import Q
from django.shortcuts import render
from .data import BUILDINGS
from .mazemap import MazeMapRouteError, get_route, node_poi_id
from indoor_nav.models import Node
from indoor_nav.pathfinding import dijkstra
from indoor_nav.path_simplification import simplify_path, format_directions
from indoor_nav.path_visualization import (
    group_segments_by_floor, get_floor_order, segments_to_svg, create_floor_transition_info
)


def find_building(building_id):
    for building in BUILDINGS:
        if building["id"] == building_id:
            return building
    return None


def _missing_error(query, node, candidates):
    if query and not node and not candidates:
        return f'No location found matching "{query}".'
    return None


def _room_code_from_text(text):
    match = re.search(r'\b([a-z]*\d+[a-z]*)\b', text.strip().lower())
    return match.group(1) if match else ''


def _building_number(text):
    match = re.search(r'building\s*(\d+)|\b(\d+)\b', text.lower())
    return (match.group(1) or match.group(2)) if match else ''


def _node_candidate(node):
    return {
        "kind": "node",
        "id": node.id,
        "label": node.label,
        "building": node.building,
        "building_number": _building_number(node.building),
        "floor": node.floor,
        "type": node.type,
        "room_code": _room_code_from_text(node.label),
    }


def _floorplan_candidates(query, node_candidates):
    room_code = _room_code_from_text(query)
    if not room_code:
        return []

    existing = {
        (candidate["building_number"], candidate["floor"], candidate["room_code"])
        for candidate in node_candidates
    }
    candidates = []

    for building in BUILDINGS:
        for floor in building["floors"]:
            for room in floor["rooms"]:
                if room["code"].lower() != room_code:
                    continue

                key = (building["number"], floor["level"], room_code)
                if key in existing:
                    continue

                candidates.append({
                    "kind": "floorplan",
                    "label": f'{room["code"]} - {room["name"]}',
                    "building": f'{building["name"]} (Building {building["number"]})',
                    "building_id": building["id"],
                    "building_number": building["number"],
                    "floor": floor["level"],
                    "floor_label": floor["label"],
                    "type": room["type"],
                    "room_code": room["code"],
                })

    return candidates


def _resolve_node(query, node_id):
    if node_id:
        return Node.objects.filter(id=node_id).first(), []
    if not query:
        return None, []

    room_code = _room_code_from_text(query)
    lookup = Q(label__icontains=query)
    if room_code:
        lookup |= Q(label__istartswith=room_code)

    matches = list(Node.objects.filter(lookup).order_by('building', 'floor', 'label'))
    node_candidates = [_node_candidate(node) for node in matches]
    candidates = node_candidates + _floorplan_candidates(query, node_candidates)

    if len(candidates) == 1 and candidates[0]["kind"] == "node":
        return matches[0], []
    return None, candidates


def _floor_room_matches(floor, query):
    matches = []
    room_code_query = _room_code_from_text(query)
    for room in floor["rooms"]:
        room_code = room["code"].lower()
        room_name = room["name"].lower()
        room_type = room["type"].lower()

        if room_code_query:
            is_match = room_code == room_code_query
        else:
            is_match = query in room_name or query in room_type

        if is_match:
            room_copy = room.copy()
            room_copy["floor_level"] = floor["level"]
            room_copy["floor_label"] = floor["label"]
            matches.append(room_copy)
    return matches


def _building_results(query):
    exact_building_number = _building_number(query) if query else ""
    if exact_building_number and any(building["number"] == exact_building_number for building in BUILDINGS):
        return [
            {"building": building, "matching_rooms": []}
            for building in BUILDINGS
            if building["number"] == exact_building_number
        ]

    results = []
    for building in BUILDINGS:
        building_matches = (
            not query
            or query in building["name"].lower()
            or query == building["number"].lower()
            or query in building["campus"].lower()
        )
        matching_rooms = []
        if query:
            for floor in building["floors"]:
                matching_rooms.extend(_floor_room_matches(floor, query))
        if building_matches or matching_rooms:
            results.append({"building": building, "matching_rooms": matching_rooms})
    return results


def _get_path_fp_coords(path, buildings):
    """
    Map each path node to its floor-plan (0–100 viewport) centre coordinate,
    grouped by building+floor so the template JS can draw per-SVG overlays.

    Returns e.g. {"b62_f1": [{"x": 48.0, "y": 52.5, "step": 1, "label": "101 – Switch Room"}, ...], ...}
    """
    if not path:
        return {}

    # Build a fast lookup:  (building_num, floor_level, room_code) → (cx, cy)
    room_lookup = {}
    for building in buildings:
        b_num = building['number']
        for floor in building['floors']:
            f_level = floor['level']
            for room in floor['rooms']:
                code = room['code'].strip().lower()
                cx = room.get('x', 0) + room.get('w', 0) / 2.0
                cy = room.get('y', 0) + room.get('h', 0) / 2.0
                room_lookup[(b_num, f_level, code)] = (cx, cy)

    result = {}
    for i, node in enumerate(path):
        m = re.search(r'\b(\d+)\b', node.building or '')
        if not m:
            continue
        b_num = m.group(1)

        label = node.label or ''
        room_code = label.split(' - ')[0].strip().lower()
        if not room_code:
            continue

        key = (b_num, node.floor, room_code)
        if key not in room_lookup:
            continue

        cx, cy = room_lookup[key]
        group_key = f"b{b_num}_f{node.floor}"
        result.setdefault(group_key, []).append({
            'x': round(cx, 2),
            'y': round(cy, 2),
            'step': i + 1,
            'label': label,
        })

    return result


def _annotate_mazemap_route_floors(features, from_floor, to_floor):
    """
    Build a flat coordinate list from MazeMap GeoJSON features, ensuring every
    coordinate carries a 'floor' label so the frontend can split the route line
    into a solid portion (destination floor) and a dashed portion (start floor).

    Priority order for the floor label of each feature's coordinates:
      1. Explicit zLevel / level in the feature's properties
      2. Third value of the coordinate tuple  (some APIs return [lon, lat, zLevel])
      3. Positional inference: first feature → from_floor, last feature → to_floor
         (MazeMap always emits separate features per floor segment, in route order)
    """
    def _zlevel(feat):
        props = feat.get("properties") or {}
        for key in ("zLevel", "z_level", "level", "zLevelId", "z"):
            val = props.get(key)
            if val is not None:
                try:
                    return str(int(round(float(val))))
                except (TypeError, ValueError):
                    return str(val)
        return None

    coords = []
    seen = set()
    n = len(features)

    for fi, feature in enumerate(features):
        z = _zlevel(feature)
        if z is None:
            # Positional fallback: first feature is on the start floor,
            # last feature is on the destination floor.
            if fi == 0:
                z = str(from_floor)
            elif fi == n - 1:
                z = str(to_floor)
            # Middle features (rare; e.g. a bridge level): leave as None →
            # treated as "not dest floor" → dashed in the frontend.

        for coord_vals in (feature.get("geometry") or {}).get("coordinates", []):
            lon, lat = coord_vals[0], coord_vals[1]
            effective_z = z
            if effective_z is None and len(coord_vals) >= 3:
                try:
                    effective_z = str(int(round(float(coord_vals[2]))))
                except (TypeError, ValueError):
                    effective_z = str(coord_vals[2])

            key = (round(lat, 7), round(lon, 7))
            if key in seen:
                continue
            seen.add(key)
            entry = {"lat": lat, "lng": lon}
            if effective_z is not None:
                entry["floor"] = effective_z
            coords.append(entry)

    return coords


def _run_route(from_q, from_id, to_q, to_id):
    from_node, from_candidates = _resolve_node(from_q, from_id)
    to_node, to_candidates = _resolve_node(to_q, to_id)
    path = path_coords = route_error = simplified_segments = floor_visualization = None

    if from_node and to_node:
        source_poi = node_poi_id(from_node)
        target_poi = node_poi_id(to_node)

        if source_poi and target_poi:
            try:
                mazemap_route = get_route(source_poi, target_poi)
                path = [from_node, to_node]
                simplified_segments = mazemap_route["directions"]
                if not simplified_segments:
                    simplified_segments = [{
                        "description": f'Follow the MazeMap route to "{to_node.label}".',
                    }]
                # For multi-floor routes, re-derive coordinates with per-coord
                # floor labels so the frontend can draw the start-floor portion
                # as dashed.  Falls back to the pre-flattened list when the
                # route stays on one floor.
                if from_node.floor and to_node.floor and from_node.floor != to_node.floor:
                    coords = _annotate_mazemap_route_floors(
                        mazemap_route["features"], from_node.floor, to_node.floor
                    )
                else:
                    coords = mazemap_route["coordinates"]
                if len(coords) >= 2:
                    path_coords = json.dumps(coords)
            except MazeMapRouteError:
                path = None

        if path is None:
            path, _ = dijkstra(from_node.id, to_node.id)
            if path is None:
                route_error = f'No path found between "{from_node.label}" and "{to_node.label}".'
            else:
                # Generate simplified path segments
                simplified_segments = simplify_path(path, angle_threshold=15.0)
                
                # Generate floor-based visualization
                if simplified_segments:
                    floor_segments = group_segments_by_floor(simplified_segments)
                    floor_order = get_floor_order(simplified_segments)
                    
                    floor_visualization = []
                    for i, floor_num in enumerate(floor_order):
                        floor_label = f"Floor {floor_num}"
                        segments = floor_segments.get(floor_label, [])
                        
                        # Generate SVG overlay for this floor
                        svg_overlay = segments_to_svg(segments)
                        
                        # Get floor transitions (stairs/elevators to next floor)
                        next_floor_transition = None
                        if i < len(floor_order) - 1:
                            next_floor = f"Floor {floor_order[i + 1]}"
                            next_floor_transition = create_floor_transition_info(
                                floor_label, next_floor, simplified_segments
                            )
                        
                        floor_visualization.append({
                            'floor': floor_label,
                            'floor_num': floor_num,
                            'segments': segments,
                            'svg_overlay': svg_overlay,
                            'next_transition': next_floor_transition
                        })
                
                coords = [
                    {'lat': n.lat, 'lng': n.lng, 'label': n.label, 'floor': n.floor}
                    for n in path if n.lat is not None and n.lng is not None
                ]
                if len(coords) >= 2:
                    path_coords = json.dumps(coords)
    else:
        route_error = (
            _missing_error(from_q, from_node, from_candidates)
            or _missing_error(to_q, to_node, to_candidates)
        )
    return from_node, from_candidates, to_node, to_candidates, path, path_coords, route_error, simplified_segments, floor_visualization


def _get_node_floor_data(node, buildings):
    """Return {'building': ..., 'floor': ..., 'svg_id': ...} for a node's building+floor, or None."""
    if not node:
        return None
    b_match = re.search(r'\b(\d+)\b', node.building or '')
    if not b_match:
        return None
    b_num = b_match.group(1)
    for building in buildings:
        if building.get('number') == b_num:
            for floor in building['floors']:
                if floor['level'] == node.floor:
                    return {
                        'building': building,
                        'floor': floor,
                        'svg_id': f'b{b_num}_f{floor["level"]}',
                    }
    return None


def _uq_map_embed_url(node=None, floor="2"):
    lat = -27.49907705145847
    lng = 153.01222576055739
    z_level = floor or "2"
    identifier = ""

    if node and node.lat and node.lng:
        lat = node.lat
        lng = node.lng
        z_level = node.floor or z_level
        identifier = node.uq_maps_identifier or ""

    params = {
        "zoom": "19.550611410027877",
        "campusId": "406",
        "lat": lat,
        "lng": lng,
        "zLevel": z_level,
        "embed": "true",
    }
    if identifier:
        params["identifier"] = identifier
    return f"https://maps.uq.edu.au/?{urlencode(params)}"


FLOOR_OPTIONS = [
    {"value": "1",  "label": "Floor 1"},
    {"value": "2",  "label": "Floor 2"},
    {"value": "2A", "label": "Floor 2A"},
    {"value": "3",  "label": "Floor 3"},
    {"value": "3A", "label": "Floor 3A"},
    {"value": "4",  "label": "Floor 4"},
    {"value": "5",  "label": "Floor 5"},
    {"value": "6",  "label": "Floor 6"},
    {"value": "7",  "label": "Floor 7"},
    {"value": "8",  "label": "Floor 8"},
    {"value": "9",  "label": "Floor 9"},
]

CAMPUS_OPTIONS = [
    {"value": "st-lucia",    "label": "St Lucia"},
    {"value": "gatton",      "label": "Gatton"},
    {"value": "herston",     "label": "Herston"},
    {"value": "dutton-park", "label": "Dutton Park"},
]


def home(request):
    q = request.GET.get("q", "").strip().lower()
    results = _building_results(q)

    selected_campus = request.GET.get("campus", "st-lucia")

    from_q = request.GET.get('from', '').strip()
    to_q = request.GET.get('to', '').strip()
    from_id = request.GET.get('from_id', '').strip()
    to_id = request.GET.get('to_id', '').strip()
    # Only compute the route when the user explicitly clicks "Get Directions"
    get_directions = bool(request.GET.get('get_directions', ''))

    from_node = to_node = path = path_coords = route_error = simplified_segments = floor_visualization = None
    from_candidates = to_candidates = []

    if to_q or to_id:
        # Always resolve the destination so Panel B can render
        to_node, to_candidates = _resolve_node(to_q, to_id)

    if from_q or from_id:
        # Resolve starting point (for display / disambiguation in Panel B)
        from_node, from_candidates = _resolve_node(from_q, from_id)

    if get_directions:
        # Full route computation — triggered only by the "Get Directions" button
        (from_node, from_candidates,
         to_node, to_candidates,
         path, path_coords, route_error,
         simplified_segments, floor_visualization) = _run_route(from_q, from_id, to_q, to_id)

    # Auto-select floor: explicit param > destination node floor > start node floor > default "1"
    selected_floor = request.GET.get("floor", "")
    if not selected_floor:
        if to_node:
            selected_floor = to_node.floor
        elif from_node:
            selected_floor = from_node.floor
        else:
            selected_floor = "1"

    # Per-node floor plan data for the split view
    from_floor_data = _get_node_floor_data(from_node, BUILDINGS)
    to_floor_data = _get_node_floor_data(to_node, BUILDINGS)

    # Gather per-building floor plan data for the selected floor level.
    def _campus_slug(raw):
        return raw.lower().replace(" ", "-")

    map_floors = []
    for building in BUILDINGS:
        if _campus_slug(building.get("campus", "")) == selected_campus:
            for floor in building["floors"]:
                if floor["level"] == selected_floor:
                    map_floors.append({"building": building, "floor": floor})
                    break

    # Create a lookup dict for floor visualization
    floor_viz_map = {}
    if floor_visualization:
        for viz_data in floor_visualization:
            floor_key = viz_data['floor_num']
            floor_viz_map[floor_key] = viz_data

    return render(request, "maps/home.html", {
        "query": request.GET.get("q", ""),
        "results": results,
        "from_q": from_q,
        "to_q": to_q,
        "from_id": from_id or (from_node.id if from_node else ''),
        "to_id": to_id or (to_node.id if to_node else ''),
        "from_node": from_node,
        "to_node": to_node,
        "from_candidates": from_candidates,
        "to_candidates": to_candidates,
        "path": path,
        "path_coords": path_coords,
        "simplified_segments": simplified_segments,
        "floor_visualization": floor_visualization,
        "floor_viz_map": floor_viz_map if floor_visualization else {},
        "route_error": route_error,
        "selected_floor": selected_floor,
        "selected_campus": selected_campus,
        "floor_options": FLOOR_OPTIONS,
        "campus_options": CAMPUS_OPTIONS,
        "map_floors": map_floors,
        "from_floor_data": from_floor_data,
        "to_floor_data": to_floor_data,
        "uq_map_embed_url": _uq_map_embed_url(to_node or from_node, selected_floor),
        "path_fp_coords_json": json.dumps(_get_path_fp_coords(path, BUILDINGS)),
    })


def building_detail(request, building_id):
    building = find_building(building_id)

    if building is None:
        return render(request, "maps/not_found.html", status=404)

    selected_floor_level = request.GET.get("floor", building["floors"][0]["level"])
    selected_room_code = request.GET.get("room", "").upper()

    current_floor = building["floors"][0]

    for floor in building["floors"]:
        if floor["level"] == selected_floor_level:
            current_floor = floor
            break

    selected_room = None

    for room in current_floor["rooms"]:
        if room["code"].upper() == selected_room_code:
            selected_room = room
            break

    return render(request, "maps/building_detail.html", {
        "building": building,
        "current_floor": current_floor,
        "selected_room": selected_room,
    })


def reminders(request):
    """Serve the smart reminders app"""
    return render(request, "maps/index.html")
