import csv
import math
from django.core.management.base import BaseCommand, CommandError
from indoor_nav.models import Node, Edge


def haversine(lat1, lng1, lat2, lng2):
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


class Command(BaseCommand):
    help = 'Import edges from a lat/lng edge CSV (e.g. MazeMap export)'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the edge CSV file')
        parser.add_argument('--building', type=str, default='', help='Filter nodes by building name substring')
        parser.add_argument('--tolerance', type=float, default=15.0, help='Max snap distance in metres (default 15)')

    def handle(self, *args, **options):
        csv_path = options['csv_file']
        tolerance = options['tolerance']
        building_filter = options['building']

        nodes_qs = Node.objects.exclude(lat=None).exclude(lng=None)
        if building_filter:
            nodes_qs = nodes_qs.filter(building__icontains=building_filter)

        nodes = list(nodes_qs)
        if not nodes:
            raise CommandError('No nodes with lat/lng found. Run import_map first.')

        self.stdout.write(f'Loaded {len(nodes)} nodes for snapping (tolerance {tolerance} m).')

        def nearest(lat, lng):
            best, best_d = None, float('inf')
            for node in nodes:
                d = haversine(lat, lng, node.lat, node.lng)
                if d < best_d:
                    best, best_d = node, d
            return best, best_d

        try:
            f = open(csv_path, newline='', encoding='utf-8')
        except FileNotFoundError:
            raise CommandError(f'File not found: {csv_path}')

        created = skipped = 0
        with f:
            for row in csv.DictReader(f):
                try:
                    from_lat = float(row['from_lat'])
                    from_lng = float(row['from_lng'])
                    to_lat = float(row['to_lat'])
                    to_lng = float(row['to_lng'])
                    weight = float(row.get('length_m') or 1.0)
                except (ValueError, KeyError) as e:
                    self.stderr.write(f'Skipping bad row: {e}')
                    skipped += 1
                    continue

                from_node, from_d = nearest(from_lat, from_lng)
                to_node, to_d = nearest(to_lat, to_lng)

                if from_d > tolerance or to_d > tolerance:
                    skipped += 1
                    continue

                if from_node == to_node:
                    skipped += 1
                    continue

                _, was_created = Edge.objects.get_or_create(
                    from_node=from_node,
                    to_node=to_node,
                    defaults={'weight': weight},
                )
                if was_created:
                    created += 1
                else:
                    skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. {created} edges created, {skipped} skipped.'
        ))