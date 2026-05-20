import math
from collections import defaultdict
from django.core.management.base import BaseCommand
from indoor_nav.models import Node, Edge


def haversine(lat1, lng1, lat2, lng2):
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _is_vertical(node):
    label = (node.label or '').lower()
    return any(kw in label for kw in ['stair', 'lift', 'elevator', 'escalator'])


class Command(BaseCommand):
    help = 'Auto-generate floor-aware edges for Building 69'

    def add_arguments(self, parser):
        parser.add_argument(
            '--threshold', type=float, default=40.0,
            help='Max same-floor connection distance in metres (default 40)'
        )
        parser.add_argument(
            '--vertical-threshold', type=float, default=12.0,
            help='Max lat/lng distance for matching stair/lift shafts across floors (default 12)'
        )
        parser.add_argument(
            '--clear', action='store_true',
            help='Delete all existing Building 69 edges before generating'
        )

    def handle(self, *args, **options):
        threshold = options['threshold']
        vertical_threshold = options['vertical_threshold']

        if options['clear']:
            deleted, _ = Edge.objects.filter(from_node__building='69').delete()
            self.stdout.write(f'Deleted {deleted} existing Building 69 edges.')

        nodes = list(
            Node.objects.filter(building='69').exclude(lat=None).exclude(lng=None)
        )
        if not nodes:
            self.stdout.write('No Building 69 nodes with lat/lng found. Run import_map first.')
            return

        self.stdout.write(f'Loaded {len(nodes)} Building 69 nodes.')

        by_floor = defaultdict(list)
        for node in nodes:
            by_floor[node.floor].append(node)

        created = 0

        # Same-floor edges
        for floor, floor_nodes in by_floor.items():
            for i, a in enumerate(floor_nodes):
                for b in floor_nodes[i + 1:]:
                    d = haversine(a.lat, a.lng, b.lat, b.lng)
                    if d > threshold:
                        continue
                    _, c1 = Edge.objects.get_or_create(
                        from_node=a, to_node=b, defaults={'weight': round(d, 2)}
                    )
                    _, c2 = Edge.objects.get_or_create(
                        from_node=b, to_node=a, defaults={'weight': round(d, 2)}
                    )
                    created += (1 if c1 else 0) + (1 if c2 else 0)

        # Cross-floor edges: connect stair/lift nodes in the same shaft
        vertical_nodes = [n for n in nodes if _is_vertical(n)]
        self.stdout.write(f'Found {len(vertical_nodes)} stair/lift nodes.')

        for i, a in enumerate(vertical_nodes):
            for b in vertical_nodes[i + 1:]:
                if a.floor == b.floor:
                    continue
                d = haversine(a.lat, a.lng, b.lat, b.lng)
                if d > vertical_threshold:
                    continue
                # Weight = 5m per floor difference (cheap so Dijkstra prefers stairs)
                floor_diff = abs(int(a.floor) - int(b.floor)) if a.floor.isdigit() and b.floor.isdigit() else 1
                w = round(5.0 * floor_diff, 2)
                _, c1 = Edge.objects.get_or_create(
                    from_node=a, to_node=b, defaults={'weight': w}
                )
                _, c2 = Edge.objects.get_or_create(
                    from_node=b, to_node=a, defaults={'weight': w}
                )
                created += (1 if c1 else 0) + (1 if c2 else 0)

        self.stdout.write(self.style.SUCCESS(f'Done. {created} edges created.'))