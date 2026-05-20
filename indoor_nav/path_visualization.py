"""
Path visualization for multi-floor navigation.

Handles grouping segments by floor and generating SVG overlays.
"""

from typing import List, Dict
from .models import Node


def group_segments_by_floor(simplified_segments: List[dict]) -> Dict[str, List[dict]]:
    """
    Group path segments by floor level.
    
    Returns dict with floor keys and segment lists:
    {
        'Floor 3': [segment1, segment2],
        'Floor 6': [segment3, segment4],
        ...
    }
    """
    floor_map = {}
    for segment in simplified_segments:
        floor = segment['end_node'].floor
        floor_label = f"Floor {floor}"
        
        if floor_label not in floor_map:
            floor_map[floor_label] = []
        floor_map[floor_label].append(segment)
    
    return floor_map


def get_floor_nodes(floor: str, simplified_segments: List[dict]) -> List[Node]:
    """
    Get all nodes on a specific floor from the segments.
    """
    nodes = []
    for segment in simplified_segments:
        start_on_floor = segment['start_node'].floor == floor
        end_on_floor = segment['end_node'].floor == floor
        
        if start_on_floor and segment['start_node'] not in nodes:
            nodes.append(segment['start_node'])
        if end_on_floor and segment['end_node'] not in nodes:
            nodes.append(segment['end_node'])
        
        # Add intermediate nodes on this floor
        for node in segment['intermediate_nodes']:
            if node.floor == floor and node not in nodes:
                nodes.append(node)
    
    return nodes


def _build_node_coordinates_list(floor_segments: List[dict]) -> List:
    """Extract all nodes in order from floor segments."""
    all_nodes = []
    for segment in floor_segments:
        if all_nodes and all_nodes[-1] and all_nodes[-1].id != segment['start_node'].id:
            all_nodes.append(None)  # Gap marker
        all_nodes.append(segment['start_node'])
        all_nodes.extend(segment['intermediate_nodes'])
        if all_nodes[-1] and all_nodes[-1].id != segment['end_node'].id:
            all_nodes.append(segment['end_node'])
    return all_nodes


def _normalize_svg_coordinates(node, floorplan_width, floorplan_height) -> tuple:
    """Convert lat/lng to SVG pixel coordinates."""
    x = (node.lng - 153.011) * 100000
    y = (-node.lat + 27.499) * 100000
    x = max(0, min(x, floorplan_width))
    y = max(0, min(y, floorplan_height))
    return x, y


def _get_color_and_indicator(turn_direction: str) -> tuple:
    """Get color and indicator symbol for a turn direction."""
    turn = turn_direction.lower()
    if 'left' in turn:
        return '#FF6B6B', ('↖' if 'sharp' in turn else '←')
    elif 'right' in turn:
        return '#4ECDC4', ('↗' if 'sharp' in turn else '→')
    else:
        return '#51247A', '↑'


def segments_to_svg(floor_segments: List[dict], floorplan_width: float = 1366, 
                    floorplan_height: float = 880) -> str:
    """
    Convert path segments on a single floor to SVG overlay.
    
    Args:
        floor_segments: List of segments on this floor
        floorplan_width: Width of the floor plan in pixels
        floorplan_height: Height of the floor plan in pixels
    
    Returns:
        SVG string with path overlay, arrows, and step numbers
    """
    if not floor_segments:
        return ""
    
    svg_parts = []
    svg_parts.append(f'<svg width="100%" height="100%" viewBox="0 0 {floorplan_width} {floorplan_height}" '
                     f'class="path-overlay" style="position: absolute; top: 0; left: 0;">')
    
    # Define arrow markers for left/right turns
    svg_parts.append('''
    <defs>
        <marker id="arrowhead-left" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
            <polygon points="5,0 10,5 5,10" fill="#FF6B6B" />
        </marker>
        <marker id="arrowhead-right" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
            <polygon points="5,0 10,5 5,10" fill="#4ECDC4" />
        </marker>
        <marker id="arrowhead-straight" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
            <polygon points="5,0 10,5 5,10" fill="#51247A" />
        </marker>
    </defs>
    ''')
    
    # Build node list and draw connections
    all_nodes = _build_node_coordinates_list(floor_segments)
    coords = []
    for node in all_nodes:
        if node is None:
            if coords:
                svg_parts.append(_draw_path_line(coords))
            coords = []
        elif node.lat and node.lng:
            x, y = _normalize_svg_coordinates(node, floorplan_width, floorplan_height)
            coords.append((x, y, node))
    
    if coords:
        svg_parts.append(_draw_path_line(coords))
    
    # Draw step numbers and turn indicators
    step_num = 1
    for segment in floor_segments:
        if segment['end_node'].lat and segment['end_node'].lng:
            x, y = _normalize_svg_coordinates(segment['end_node'], floorplan_width, floorplan_height)
            color, indicator = _get_color_and_indicator(segment['turn_direction'])
            
            # Draw circle for step
            svg_parts.append(f'<circle cx="{x}" cy="{y}" r="12" fill="white" stroke="{color}" stroke-width="2" />')
            
            # Draw step number
            svg_parts.append(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" '
                           f'class="step-label" font-size="10" font-weight="bold" fill="{color}">{step_num}</text>')
            
            # Draw turn indicator below step number
            svg_parts.append(f'<text x="{x}" y="{y + 20}" text-anchor="middle" class="turn-indicator" '
                           f'font-size="8" fill="{color}">{indicator}</text>')
            
            step_num += 1
    
    svg_parts.append('</svg>')
    return ''.join(svg_parts)


def _draw_path_line(coords: List[tuple]) -> str:
    """Draw a continuous line through coordinates."""
    if len(coords) < 2:
        return ""
    
    points = ' '.join(f"{x},{y}" for x, y, _ in coords)
    return f'<polyline points="{points}" fill="none" stroke="#51247A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity="0.7" />'


def get_floor_order(simplified_segments: List[dict]) -> List[str]:
    """Get floors in order (ascending or descending based on path)."""
    floors = []
    for segment in simplified_segments:
        floor = segment['end_node'].floor
        if floor not in floors:
            floors.append(floor)
    
    # Try to sort numerically
    try:
        floors = sorted(floors, key=lambda f: int(f) if f.isdigit() else float(f))
    except (ValueError, TypeError):
        # If sorting fails, keep original order
        pass
    
    return floors


def create_floor_transition_info(floor_a: str, floor_b: str, segments: List[dict]) -> dict:
    """
    Find the stair/elevator connection between two floors.
    """
    for segment in segments:
        if (segment['start_node'].floor == floor_a and segment['end_node'].floor == floor_b) or \
           (segment['start_node'].floor == floor_b and segment['end_node'].floor == floor_a):
            
            # Find the stair/elevator node
            transition_node = None
            if segment['end_node'].type in ['stairs', 'elevator']:
                transition_node = segment['end_node']
            elif segment['start_node'].type in ['stairs', 'elevator']:
                transition_node = segment['start_node']
            
            return {
                'from_floor': floor_a,
                'to_floor': floor_b,
                'transition_node': transition_node,
                'type': 'stairs' if transition_node and 'stair' in transition_node.type.lower() else 'elevator'
            }
    
    return {}
