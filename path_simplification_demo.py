"""
Path Simplification Demo & Test

This script demonstrates how the path simplification works.
Run it with: python manage.py shell < path_simplification_demo.py
"""

from indoor_nav.pathfinding import dijkstra
from indoor_nav.path_simplification import simplify_path, format_directions
from indoor_nav.models import Node

# Example: Find path from 501 Hot Desk to 315 Wet Lab
# Adjust these node IDs to match your actual database
try:
    # Get the actual path from pathfinding
    start_node = Node.objects.get(label__icontains="501")
    end_node = Node.objects.get(label__icontains="315")
    
    print(f"\n{'='*70}")
    print(f"Finding path: {start_node.label} → {end_node.label}")
    print(f"{'='*70}\n")
    
    path, distance = dijkstra(start_node.id, end_node.id)
    
    if path:
        print(f"Full path has {len(path)} nodes\n")
        
        # Show all nodes in the path
        print("FULL PATH:")
        print("-" * 70)
        for i, node in enumerate(path, 1):
            print(f"{i:2d}. {node.label:40s} ({node.type:15s}) Floor {node.floor}")
        
        # Simplify the path
        print(f"\n\nSIMPLIFIED PATH:")
        print("-" * 70)
        simplified = simplify_path(path, angle_threshold=15.0)
        
        for segment in simplified:
            print(f"\nSegment {segment['segment_index']}:")
            print(f"  Description: {segment['description']}")
            print(f"  Turn direction: {segment['turn_direction']}")
            print(f"  Start: {segment['start_node'].label}")
            print(f"  End: {segment['end_node'].label}")
            if segment['intermediate_nodes']:
                print(f"  Passes through {len(segment['intermediate_nodes'])} locations:")
                for node in segment['intermediate_nodes']:
                    print(f"    - {node.label}")
        
        # Show formatted directions
        print(f"\n\nHUMAN-READABLE DIRECTIONS:")
        print("-" * 70)
        directions = format_directions(simplified, include_node_details=True)
        print(directions)
        
        print(f"\n\nSUMMARY:")
        print("-" * 70)
        print(f"Original path steps: {len(path) - 1}")
        print(f"Simplified segments: {len(simplified)}")
        print(f"Compression ratio: {(len(path) - 1) / len(simplified):.1f}x")
        
    else:
        print("No path found!")
        
except Node.DoesNotExist as e:
    print(f"Error: {e}")
    print("The node IDs in this example may not match your database.")
    print("Try updating the node labels in the script to match your database.")
