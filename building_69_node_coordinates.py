"""
Building 69 Node ID to Coordinate Mapping

Maps database node IDs to coordinate positions based on PDF floor plan analysis.
"""

# Node ID to coordinate mapping (floor: {node_id: coordinate_dict})
NODE_COORDINATES = {
    "2": {  # Level 2
        "1192707": {"x": 50, "y": 4, "w": 10, "h": 6, "arm": "north", "room": "207B"},
        "1192722": {"x": 62, "y": 4, "w": 10, "h": 6, "arm": "north", "room": "207A"},
        "1192725": {"x": 56, "y": 10, "w": 12, "h": 6, "arm": "north", "room": "207"},
        "1192718": {"x": 40, "y": 6, "w": 12, "h": 8, "arm": "north", "room": "206B"},
        "1192727": {"x": 40, "y": 14, "w": 12, "h": 8, "arm": "north", "room": "206A"},
        "1192728": {"x": 54, "y": 18, "w": 12, "h": 4, "arm": "north", "room": "206"},
        
        "1192709": {"x": 72, "y": 28, "w": 20, "h": 14, "arm": "east", "room": "209"},
        "1192715": {"x": 72, "y": 44, "w": 20, "h": 14, "arm": "east", "room": "208"},
        
        "1192719": {"x": 30, "y": 72, "w": 12, "h": 10, "arm": "south", "room": "225"},
        
        "1192721": {"x": 12, "y": 24, "w": 4, "h": 50, "arm": "west", "room": "299"},
        "1192716": {"x": 8, "y": 24, "w": 4, "h": 50, "arm": "west", "room": "298"},
        
        "1192708": {"x": 25, "y": 28, "w": 15, "h": 8, "arm": "center", "room": "290"},
        "1192710": {"x": 25, "y": 38, "w": 15, "h": 8, "arm": "center", "room": "295"},
        "1192711": {"x": 38, "y": 35, "w": 12, "h": 10, "arm": "center", "room": "294"},
        "1192712": {"x": 8, "y": 24, "w": 4, "h": 50, "arm": "center", "room": "297"},
        "1192717": {"x": 28, "y": 50, "w": 8, "h": 6, "arm": "center", "room": "211"},
        "1192724": {"x": 38, "y": 50, "w": 8, "h": 6, "arm": "center", "room": "212"},
        "1192726": {"x": 48, "y": 50, "w": 8, "h": 6, "arm": "center", "room": "213"},
        "1192714": {"x": 45, "y": 28, "w": 8, "h": 8, "arm": "center", "room": "296"},
        "1192713": {"x": 45, "y": 38, "w": 12, "h": 6, "arm": "center", "room": "207C"},
        "1192720": {"x": 32, "y": 60, "w": 10, "h": 6, "arm": "center", "room": "210"},
    },
    
    "3": {  # Level 3
        "1192729": {"x": 35, "y": 6, "w": 25, "h": 14, "arm": "north", "room": "316"},
        "1192730": {"x": 62, "y": 6, "w": 12, "h": 14, "arm": "north", "room": "315"},
        
        "1192735": {"x": 72, "y": 32, "w": 18, "h": 14, "arm": "east", "room": "304"},
        "1192740": {"x": 72, "y": 48, "w": 18, "h": 14, "arm": "east", "room": "305"},
        
        "1192734": {"x": 12, "y": 24, "w": 4, "h": 50, "arm": "west", "room": "399"},
        "1192739": {"x": 8, "y": 24, "w": 4, "h": 50, "arm": "west", "room": "398"},
        
        "1192731": {"x": 28, "y": 50, "w": 8, "h": 6, "arm": "center", "room": "330A"},
        "1192732": {"x": 36, "y": 50, "w": 10, "h": 6, "arm": "center", "room": "330"},
        "1192736": {"x": 48, "y": 50, "w": 8, "h": 6, "arm": "center", "room": "330B"},
        "1192733": {"x": 42, "y": 42, "w": 8, "h": 6, "arm": "center", "room": "321A"},
        "1192742": {"x": 52, "y": 42, "w": 8, "h": 6, "arm": "center", "room": "322"},
        "1192741": {"x": 8, "y": 24, "w": 4, "h": 50, "arm": "center", "room": "397"},
        "1192737": {"x": 22, "y": 35, "w": 15, "h": 8, "arm": "center", "room": "395"},
        "1192743": {"x": 45, "y": 28, "w": 8, "h": 8, "arm": "center", "room": "396"},
        "1192738": {"x": 28, "y": 60, "w": 10, "h": 6, "arm": "center", "room": "331"},
    }
}

def get_node_coordinates(floor, node_id):
    """Get coordinate data for a specific node ID."""
    if floor in NODE_COORDINATES:
        return NODE_COORDINATES[floor].get(str(node_id))
    return None

def get_floor_node_coordinates(floor):
    """Get all node coordinates for a floor."""
    return NODE_COORDINATES.get(floor, {})

def get_populated_floors():
    """Get list of floors with coordinate mappings."""
    return list(NODE_COORDINATES.keys())
