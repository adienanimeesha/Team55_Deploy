import math
from typing import List, Tuple
from .models import Node


def calculate_bearing(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate compass bearing between two points (0-360 degrees).
    Returns angle from north, clockwise.
    """
    dlng = lng2 - lng1
    y = math.sin(math.radians(dlng)) * math.cos(math.radians(lat2))
    x = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - \
        math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dlng))
    bearing = math.degrees(math.atan2(y, x))
    return (bearing + 360) % 360


def angle_difference(angle1: float, angle2: float) -> float:
    """
    Calculate minimum angle difference between two bearings (0-180).
    """
    diff = abs(angle2 - angle1)
    return min(diff, 360 - diff)


def simplify_path(nodes: List[Node], angle_threshold: float = 15.0) -> List[dict]:
    """
    Simplify a path by grouping collinear segments.
    
    Args:
        nodes: List of Node objects in order (from pathfinding)
        angle_threshold: Max angle change to consider nodes collinear (degrees)
    
    Returns:
        List of segment dictionaries with simplified instructions:
        [
            {
                'segment_index': 1,
                'start_node': Node,
                'end_node': Node,
                'intermediate_nodes': [Node, ...],  # nodes passed through
                'turn_direction': 'left', 'right', 'straight', etc.
                'description': 'Go straight through rooms X, Y, Z until you reach W'
            },
            ...
        ]
    """
    if len(nodes) < 2:
        return [{'segment_index': 1, 'start_node': nodes[0], 'end_node': nodes[0], 
                 'intermediate_nodes': [], 'turn_direction': 'straight', 'description': 'You have arrived'}]
    
    segments = []
    segment_start_idx = 0
    segment_direction = None
    prev_segment_direction = None
    
    for i in range(len(nodes) - 1):
        if i == 0:
            # Calculate initial direction
            segment_direction = calculate_bearing(
                nodes[i].lat, nodes[i].lng,
                nodes[i + 1].lat, nodes[i + 1].lng
            )
            continue
        
        # Calculate direction to next node
        current_direction = calculate_bearing(
            nodes[i].lat, nodes[i].lng,
            nodes[i + 1].lat, nodes[i + 1].lng
        )
        
        # Check if direction significantly changed
        dir_change = angle_difference(segment_direction, current_direction)
        
        # Start new segment if direction changed or last node
        if dir_change > angle_threshold or i == len(nodes) - 2:
            # Create segment
            segment_end_idx = i + 1 if i == len(nodes) - 2 else i
            
            segment = _create_segment(
                nodes,
                segment_start_idx,
                segment_end_idx,
                segment_direction,
                len(segments) + 1,
                prev_segment_direction
            )
            segments.append(segment)
            
            # Save this direction for next segment's turn calculation
            prev_segment_direction = segment_direction
            
            # Start new segment
            if i < len(nodes) - 2:
                segment_start_idx = i
                segment_direction = current_direction
    
    return segments


def _create_segment(nodes: List[Node], start_idx: int, end_idx: int, 
                   bearing: float, segment_num: int, prev_bearing: float = None) -> dict:
    """Create a simplified segment description."""
    
    start_node = nodes[start_idx]
    end_node = nodes[end_idx]
    intermediate_nodes = nodes[start_idx + 1:end_idx]
    
    # Determine turn direction
    if prev_bearing is None:
        turn_direction = "straight"
    else:
        angle_diff = bearing - prev_bearing
        # Normalize to -180 to 180
        while angle_diff > 180:
            angle_diff -= 360
        while angle_diff < -180:
            angle_diff += 360
        
        if abs(angle_diff) < 15:
            turn_direction = "straight"
        elif angle_diff > 0:  # Positive = clockwise = right turn
            if angle_diff > 100:
                turn_direction = "right (sharp)"
            else:
                turn_direction = "right"
        else:  # Negative = counter-clockwise = left turn
            if angle_diff < -100:
                turn_direction = "left (sharp)"
            else:
                turn_direction = "left"
    
    # Build description
    if len(intermediate_nodes) == 0:
        description = f"Go {turn_direction} to {end_node.label}"
    else:
        # List intermediate rooms
        intermediate_labels = [n.label for n in intermediate_nodes if n.type not in ['corridor']]
        if intermediate_labels:
            rooms_str = ', '.join(intermediate_labels)
            if segment_num == 1:
                description = f"Go straight through {rooms_str} until you reach {end_node.label}"
            else:
                description = f"Turn {turn_direction} through {rooms_str} until you reach {end_node.label}"
        else:
            description = f"Go {turn_direction} until you reach {end_node.label}"
    
    return {
        'segment_index': segment_num,
        'start_node': start_node,
        'end_node': end_node,
        'intermediate_nodes': intermediate_nodes,
        'bearing': bearing,
        'turn_direction': turn_direction,
        'description': description
    }


def format_directions(segments: List[dict], include_node_details: bool = False) -> str:
    """
    Format simplified segments into human-readable directions.
    
    Example output:
    1. Go northeast straight through rooms 212, 211, 210 until you reach 208
    2. Turn right (southeast) up the stairs to 698
    3. Go north along the corridor until you reach 315
    """
    lines = []
    for seg in segments:
        desc = seg['description']
        if include_node_details:
            desc += f" ({seg['start_node'].building} Floor {seg['start_node'].floor})"
        lines.append(f"{seg['segment_index']}. {desc}")
    
    return '\n'.join(lines)
