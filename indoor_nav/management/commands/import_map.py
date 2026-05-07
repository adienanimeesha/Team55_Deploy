import csv
from django.core.management.base import BaseCommand, CommandError
from indoor_nav.models import Node, Edge


class Command(BaseCommand):
    help = 'Import nodes and edges from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        path = options['csv_file']

        try:
            file = open(path, newline='', encoding='utf-8')
        except FileNotFoundError:
            raise CommandError(f'File not found: {path}')

        with file:
            reader = csv.DictReader(file)
            nodes_created = 0
            edges_created = 0

            rows = list(reader)

            for row in rows:
                if not row.get('from_id') and not row.get('to_id'):
                    Node.objects.update_or_create(
                        id=row['id'],
                        defaults={
                            'building': row.get('building', ''),
                            'floor': row.get('floor', ''),
                            'type': row.get('type', ''),
                            'label': row.get('label', ''),
                            'lat': float(row['lat']) if row.get('lat') else None,
                            'lng': float(row['lng']) if row.get('lng') else None,
                            'uq_maps_identifier': row.get('uq_maps_identifier', ''),
                        }
                    )
                    nodes_created += 1

            for row in rows:
                if row.get('from_id') and row.get('to_id'):
                    try:
                        from_node = Node.objects.get(id=row['from_id'])
                        to_node = Node.objects.get(id=row['to_id'])
                        Edge.objects.get_or_create(from_node=from_node, to_node=to_node)
                        edges_created += 1
                    except Node.DoesNotExist as e:
                        self.stderr.write(f'Skipping edge {row["from_id"]} → {row["to_id"]}: {e}')

        self.stdout.write(self.style.SUCCESS(
            f'Imported {nodes_created} nodes and {edges_created} edges'
        ))