"""
Django management command to generate Building 69 SVG floor plan visualizations
and validate room layouts against the coordinate mapping.
"""

import json
from django.core.management.base import BaseCommand, CommandError
from indoor_nav.models import Node
from building_69_coordinate_mapping import (
    FLOOR_OUTLINES, ROOM_COORDINATES, get_floor_outline, get_all_room_coordinates
)
from building_69_node_coordinates import (
    get_floor_node_coordinates, get_node_coordinates
)


class Command(BaseCommand):
    help = 'Generate SVG visualizations of Building 69 floor layouts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--floor',
            type=str,
            default='all',
            help='Floor number to visualize (or "all" for all floors)'
        )
        parser.add_argument(
            '--output-dir',
            type=str,
            default='.',
            help='Output directory for SVG files'
        )
        parser.add_argument(
            '--validate',
            action='store_true',
            help='Validate room data against database nodes'
        )
        parser.add_argument(
            '--json',
            action='store_true',
            help='Output coordinate data as JSON instead of SVG'
        )

    def handle(self, *args, **options):
        floor_num = options['floor']
        output_dir = options['output_dir']
        validate = options['validate']
        json_output = options['json']

        floors = [floor_num] if floor_num != 'all' else list(FLOOR_OUTLINES.keys())

        for floor in floors:
            if json_output:
                self._output_json(floor)
            else:
                filename = f"{output_dir}/B69_L{floor}_layout.svg"
                self._generate_svg(floor, filename, validate)

    def _generate_svg(self, floor, filename, validate=False):
        """Generate SVG visualization of floor layout."""
        outline = get_floor_outline(floor)
        if not outline:
            self.stderr.write(f"No outline data for floor {floor}")
            return

        # Use node_id based coordinates
        node_coords = get_floor_node_coordinates(floor)
        nodes = Node.objects.filter(building='69', floor=floor)

        # SVG dimensions
        svg_width, svg_height = 1200, 1200
        scale = 10  # pixels per unit

        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .floor-bg {{ fill: #f5f5f5; stroke: #333; stroke-width: 2; }}
    .room {{ fill: #e8f4f8; stroke: #666; stroke-width: 1; }}
    .room:hover {{ fill: #b8e0f0; }}
    .stair {{ fill: #ffcccc; stroke: #999; stroke-width: 1; }}
    .lift {{ fill: #ccffcc; stroke: #999; stroke-width: 1; }}
    .utility {{ fill: #ffffcc; stroke: #999; stroke-width: 1; }}
    .text {{ font-family: Arial; font-size: 10px; }}
    .label {{ font-size: 8px; fill: #333; }}
    .room-label {{ font-size: 9px; fill: #000; font-weight: bold; }}
  </style>
  
  <g id="floor-{floor}">
    <text x="20" y="40" class="text" style="font-size: 24px; font-weight: bold;">
      Building 69 - {outline.get('name', f'Level {floor}')}
    </text>
    
    <!-- Floor outline (cross shape) -->
'''

        # Draw floor regions
        if 'north_arm' in outline:
            svg_content += self._draw_region(
                outline['north_arm'], 'North Arm', scale, 'floor-bg'
            )
        if 'south_arm' in outline:
            svg_content += self._draw_region(
                outline['south_arm'], 'South Arm', scale, 'floor-bg'
            )
        if 'east_arm' in outline:
            svg_content += self._draw_region(
                outline['east_arm'], 'East Arm', scale, 'floor-bg'
            )
        if 'west_arm' in outline:
            svg_content += self._draw_region(
                outline['west_arm'], 'West Arm', scale, 'floor-bg'
            )
        if 'center_junction' in outline:
            svg_content += self._draw_region(
                outline['center_junction'], 'Center', scale, 'floor-bg'
            )
        if 'east_extension' in outline:
            svg_content += self._draw_region(
                outline['east_extension'], 'East Extension', scale, 'floor-bg'
            )

        # Draw rooms using node_id coordinates
        svg_content += '\n    <!-- Rooms -->\n'
        for node_id, coords in node_coords.items():
            node = nodes.filter(id=node_id).first()
            if not node:
                continue

            room_class = 'stair' if 'stair' in node.label.lower() else \
                        'lift' if 'lift' in node.label.lower() else \
                        'utility' if any(kw in node.label.lower() for kw in ['plant', 'riser', 'circulation']) else \
                        'room'
            
            svg_content += self._draw_room_node(node_id, node.label, coords, scale, room_class)

        svg_content += '  </g>\n</svg>'

        with open(filename, 'w') as f:
            f.write(svg_content)

        self.stdout.write(
            self.style.SUCCESS(f'Generated SVG: {filename}')
        )

        if validate:
            self._validate_floor(floor, nodes, node_coords)

    def _output_json(self, floor):
        """Output coordinate data as JSON."""
        outline = get_floor_outline(floor)
        rooms = get_all_room_coordinates(floor)

        data = {
            "floor": floor,
            "outline": outline,
            "rooms": rooms,
            "node_count": Node.objects.filter(building='69', floor=floor).count(),
        }

        self.stdout.write(json.dumps(data, indent=2))

    def _draw_region(self, region, label, scale, css_class):
        """Generate SVG for a floor region."""
        if not region:
            return ''

        x = region['x'] * scale + 50
        y = region['y'] * scale + 100
        w = region['w'] * scale
        h = region['h'] * scale

        return f'''    <rect x="{x}" y="{y}" width="{w}" height="{h}" class="{css_class}"/>
    <text x="{x + 10}" y="{y + 20}" class="label">{label}</text>
'''

    def _draw_room(self, room_id, coords, scale, css_class):
        """Generate SVG for a room."""
        x = coords['x'] * scale + 50
        y = coords['y'] * scale + 100
        w = coords['w'] * scale
        h = coords['h'] * scale

        # Get database node for validation
        node = Node.objects.filter(building='69', id=room_id).first()
        title = f"{room_id}: {node.label if node else coords.get('label', '')}"

        return f'''    <rect x="{x}" y="{y}" width="{w}" height="{h}" class="{css_class}">
      <title>{title}</title>
    </rect>
    <text x="{x + 5}" y="{y + 15}" class="room-label">{room_id}</text>
'''

    def _draw_room_node(self, node_id, label, coords, scale, css_class):
        """Generate SVG for a room by node ID."""
        x = coords['x'] * scale + 50
        y = coords['y'] * scale + 100
        w = coords['w'] * scale
        h = coords['h'] * scale

        # Extract room number from label
        room_num = coords.get('room', node_id)
        title = f"{node_id}: {label}"

        return f'''    <rect x="{x}" y="{y}" width="{w}" height="{h}" class="{css_class}">
      <title>{title}</title>
    </rect>
    <text x="{x + 5}" y="{y + 15}" class="room-label">{room_num}</text>
'''

    def _validate_floor(self, floor, nodes, rooms):
        """Validate floor layout against database."""
        self.stdout.write(f'\nValidation for Floor {floor}:')
        self.stdout.write(f'  Database nodes: {nodes.count()}')
        self.stdout.write(f'  Mapped rooms: {len(rooms)}')

        # Find unmapped rooms
        db_ids = set(str(n.id) for n in nodes)
        mapped_ids = set(rooms.keys())

        unmapped = db_ids - mapped_ids
        if unmapped:
            self.stdout.write(f'  Unmapped rooms ({len(unmapped)}): {list(unmapped)[:5]}...')
        
        # Report stats by arm
        arms = {}
        for node_id, coords in rooms.items():
            arm = coords.get('arm', 'unknown')
            if arm not in arms:
                arms[arm] = []
            arms[arm].append(node_id)
        
        for arm in sorted(arms.keys()):
            self.stdout.write(f'  {arm.title()} arm: {len(arms[arm])} rooms')
