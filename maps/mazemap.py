import requests


ROUTING_BASE_URL = "https://api.mazemap.com/routing"
REQUEST_TIMEOUT_SECONDS = 10


class MazeMapRouteError(Exception):
    pass


def node_poi_id(node):
    if not node:
        return None
    if getattr(node, "poi_id", None):
        return node.poi_id
    return int(node.id) if str(node.id).isdigit() else None


def get_route(source_poi_id, target_poi_id):
    params = {
        "srid": 4326,
        "sourcepoi": source_poi_id,
        "targetpoi": target_poi_id,
        "lang": "en",
    }
    path_data = _get_json(f"{ROUTING_BASE_URL}/path/", params)
    directions_data = _get_json(f"{ROUTING_BASE_URL}/directions/", params)

    features = path_data.get("path", {}).get("features", [])
    if not features:
        raise MazeMapRouteError("MazeMap did not return a route path.")

    metrics = path_data.get("pathMetrics", {})
    distance_m = float(metrics.get("distance", 0) or 0)
    # Walking speed ≈ 1.4 m/s = 84 m/min; minimum 1 min shown
    walking_minutes = max(1, round(distance_m / 84)) if distance_m > 0 else None

    return {
        "features": features,
        "metrics": metrics,
        "distance_m": distance_m,
        "walking_minutes": walking_minutes,
        "coordinates": _flatten_feature_coordinates(features),
        "directions": _extract_directions(directions_data),
    }


def _get_json(url, params):
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise MazeMapRouteError(f"MazeMap request failed: {exc}") from exc
    return response.json()


def _feature_zlevel(feature):
    """Return the z-level (floor) for a MazeMap route feature, or None."""
    props = feature.get("properties") or {}
    for key in ("zLevel", "z_level", "level", "zLevelId", "z"):
        if props.get(key) is not None:
            return props[key]
    return None


def _normalise_floor(z):
    """Convert a raw z-level value to a plain floor string, e.g. 2.0 → '2'."""
    try:
        return str(int(round(float(z))))
    except (TypeError, ValueError):
        return str(z)


def _coord_entry(lon, lat, z):
    """Build a single coordinate dict, optionally including floor info."""
    entry = {"lat": lat, "lng": lon}
    if z is not None:
        entry["floor"] = _normalise_floor(z)
    return entry


def _flatten_feature_coordinates(features):
    coords = []
    seen = set()
    for feature in features:
        z = _feature_zlevel(feature)
        for coord_vals in (feature.get("geometry") or {}).get("coordinates", []):
            lon, lat = coord_vals[0], coord_vals[1]
            # Some responses embed z-level as the third coordinate value.
            effective_z = coord_vals[2] if (z is None and len(coord_vals) >= 3) else z
            key = (round(lat, 7), round(lon, 7))
            if key in seen:
                continue
            seen.add(key)
            coords.append(_coord_entry(lon, lat, effective_z))
    return coords


def _extract_directions(data):
    directions = []
    for route in data.get("routes", []):
        for leg in route.get("legs", []):
            for step in leg.get("steps", []):
                instruction = step.get("instruction")
                if instruction:
                    directions.append({"description": instruction})
    return directions
