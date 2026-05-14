import csv
from django.core.management.base import BaseCommand, CommandError
from indoor_nav.models import Node, Edge


class Command(BaseCommand):
    help = 'Import nodes and edges from one or more CSV files'

    def add_arguments(self, parser):
        parser.add_argument('csv_files', nargs='+', type=str, help='Path to CSV file(s)')

    def handle(self, *args, **options):
        total_nodes = 0
        total_edges = 0

        for path in options['csv_files']:
            self.stdout.write(f'Importing {path}...')
            try:
                file = open(path, newline='', encoding='utf-8')
            except FileNotFoundError:
                raise CommandError(f'File not found: {path}')

            with file:
                reader = csv.DictReader(file)
                rows = list(reader)
                columns = reader.fieldnames or []

            is_edges_only = 'from_id' in columns and 'id' not in columns
            if is_edges_only:
                node_rows = []
                edge_rows = rows
            else:
                node_rows = [r for r in rows if not r.get('from_id') and not r.get('to_id')]
                edge_rows = [r for r in rows if r.get('from_id') and r.get('to_id')]

            nodes_created = sum(self._import_node(r) for r in node_rows)
            edges_created = sum(self._import_edge(r) for r in edge_rows)
            total_nodes += nodes_created
            total_edges += edges_created

            self.stdout.write(f'  {nodes_created} nodes, {edges_created} edges')

        self.stdout.write(self.style.SUCCESS(
            f'Done. Total: {total_nodes} nodes, {total_edges} edges'
        ))

    def _import_node(self, row):
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
        return 1

    def _import_edge(self, row):
        try:
            from_node = Node.objects.get(id=row['from_id'])
            to_node = Node.objects.get(id=row['to_id'])
            weight = float(row['weight']) if row.get('weight') else 1.0
            Edge.objects.get_or_create(
                from_node=from_node,
                to_node=to_node,
                defaults={'weight': weight},
            )
            return 1
        except Node.DoesNotExist as e:
            self.stderr.write(f'Skipping edge {row["from_id"]} → {row["to_id"]}: {e}')
            return 0