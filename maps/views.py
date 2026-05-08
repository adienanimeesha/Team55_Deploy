from django.shortcuts import render
from .data import BUILDINGS


def find_building(building_id):
    for building in BUILDINGS:
        if building["id"] == building_id:
            return building
    return None


def home(request):
    query = request.GET.get("q", "").strip().lower()
    results = []

    for building in BUILDINGS:
        building_matches = (
            query == ""
            or query in building["name"].lower()
            or query in building["number"].lower()
            or query in building["campus"].lower()
        )

        matching_rooms = []

        for floor in building["floors"]:
            for room in floor["rooms"]:
                room_matches = (
                    query != ""
                    and (
                        query in room["code"].lower()
                        or query in room["name"].lower()
                        or query in room["type"].lower()
                    )
                )

                if room_matches:
                    room_copy = room.copy()
                    room_copy["floor_level"] = floor["level"]
                    room_copy["floor_label"] = floor["label"]
                    matching_rooms.append(room_copy)

        if building_matches or matching_rooms:
            results.append({
                "building": building,
                "matching_rooms": matching_rooms,
            })

    return render(request, "maps/home.html", {
        "query": request.GET.get("q", ""),
        "results": results,
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