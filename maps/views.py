import json
import re
from django.db.models import Q
from django.shortcuts import render
from .data import BUILDINGS
from indoor_nav.models import Node
from indoor_nav.pathfinding import dijkstra


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
    for room in floor["rooms"]:
        if query in room["code"].lower() or query in room["name"].lower() or query in room["type"].lower():
            room_copy = room.copy()
            room_copy["floor_level"] = floor["level"]
            room_copy["floor_label"] = floor["label"]
            matches.append(room_copy)
    return matches


def _building_results(query):
    results = []
    for building in BUILDINGS:
        building_matches = (
            not query
            or query in building["name"].lower()
            or query in building["number"].lower()
            or query in building["campus"].lower()
        )
        matching_rooms = []
        if query:
            for floor in building["floors"]:
                matching_rooms.extend(_floor_room_matches(floor, query))
        if building_matches or matching_rooms:
            results.append({"building": building, "matching_rooms": matching_rooms})
    return results


def _run_route(from_q, from_id, to_q, to_id):
    from_node, from_candidates = _resolve_node(from_q, from_id)
    to_node, to_candidates = _resolve_node(to_q, to_id)
    path = path_coords = route_error = None

    if from_node and to_node:
        path, _ = dijkstra(from_node.id, to_node.id)
        if path is None:
            route_error = f'No path found between "{from_node.label}" and "{to_node.label}".'
        else:
            coords = [
                {'lat': n.lat, 'lng': n.lng, 'label': n.label}
                for n in path if n.lat is not None and n.lng is not None
            ]
            if len(coords) >= 2:
                path_coords = json.dumps(coords)
    else:
        route_error = (
            _missing_error(from_q, from_node, from_candidates)
            or _missing_error(to_q, to_node, to_candidates)
        )
    return from_node, from_candidates, to_node, to_candidates, path, path_coords, route_error


def home(request):
    q = request.GET.get("q", "").strip().lower()
    results = _building_results(q)

    from_q = request.GET.get('from', '').strip()
    to_q = request.GET.get('to', '').strip()
    from_id = request.GET.get('from_id', '').strip()
    to_id = request.GET.get('to_id', '').strip()

    from_node = to_node = path = path_coords = route_error = None
    from_candidates = to_candidates = []

    if from_q or from_id or to_q or to_id:
        from_node, from_candidates, to_node, to_candidates, path, path_coords, route_error = (
            _run_route(from_q, from_id, to_q, to_id)
        )

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
        "route_error": route_error,
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
