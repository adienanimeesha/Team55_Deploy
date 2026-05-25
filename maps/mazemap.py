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

    return {
        "features": features,
        "metrics": path_data.get("pathMetrics", {}),
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


def _flatten_feature_coordinates(features):
    coords = []
    seen = set()
    for feature in features:
        for lon, lat in feature.get("geometry", {}).get("coordinates", []):
            key = (lat, lon)
            if key in seen:
                continue
            seen.add(key)
            coords.append({"lat": lat, "lng": lon})
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
