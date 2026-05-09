import math
from collections import defaultdict
from django.core.management.base import BaseCommand
from indoor_nav.models import Node, Edge


def haversine(lat1, lng1, lat2, lng2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def make_edge(a, b, weight):
    _, created = Edge.objects.get_or_create(from_node=a, to_node=b, defaults={'weight': weight})
    return created


class Command(BaseCommand):
    help = 'Auto-generate edges from node proximity'

    def add_arguments(self, parser):
        parser.add_argument('--threshold', type=float, default=50.0, help='Max distance (m) for same-floor edges')
        parser.add_argument('--stair-threshold', type=float, default=30.0, help='Max distance (m) to match staircases across floors')

    def handle(self, *args, **options):
        threshold = options['threshold']
        stair_threshold = options['stair_threshold']

        nodes = list(Node.objects.exclude(lat=None).exclude(lng=None))
        created = 0

        by_floor = defaultdict(list)
        by_building = defaultdict(list)
        vertical_nodes = []

        for node in nodes:
            by_floor[(node.building, node.floor)].append(node)
            by_building[node.building].append(node)
            if node.type in ('stairs', 'lift'):
                vertical_nodes.append(node)

        # Same floor, same building
        for floor_nodes in by_floor.values():
            for i, a in enumerate(floor_nodes):
                for b in floor_nodes[i + 1:]:
                    dist = haversine(a.lat, a.lng, b.lat, b.lng)
                    if dist <= threshold:
                        if make_edge(a, b, dist):
                            created += 1

        # Stairs/lifts across floors (same building, same staircase)
        by_building_vertical = defaultdict(list)
        for node in vertical_nodes:
            by_building_vertical[node.building].append(node)

        for vert_nodes in by_building_vertical.values():
            for i, a in enumerate(vert_nodes):
                for b in vert_nodes[i + 1:]:
                    if a.floor != b.floor:
                        dist = haversine(a.lat, a.lng, b.lat, b.lng)
                        if dist <= stair_threshold:
                            if make_edge(a, b, dist + 15):
                                created += 1

        # Inter-building: connect closest node pair between each building
        buildings = list(by_building.keys())
        for i, b1 in enumerate(buildings):
            for b2 in buildings[i + 1:]:
                min_dist = float('inf')
                closest = None
                for a in by_building[b1]:
                    for b in by_building[b2]:
                        dist = haversine(a.lat, a.lng, b.lat, b.lng)
                        if dist < min_dist:
                            min_dist = dist
                            closest = (a, b)
                if closest:
                    if make_edge(closest[0], closest[1], min_dist):
                        created += 1
                    self.stdout.write(
                        f'Inter-building: {closest[0].id} ({b1}) ↔ {closest[1].id} ({b2}) — {min_dist:.1f}m'
                    )

        self.stdout.write(self.style.SUCCESS(f'Created {created} edges'))