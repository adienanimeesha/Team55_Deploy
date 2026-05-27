"""
Building 69 Coordinate Mapping

Based on detailed PDF floor plan analysis (0069-1 through 0069-9), this module
defines the precise coordinate positions for all rooms in Building 69, accounting
for the cross-shaped layout and floor-specific variations.

Coordinate System:
- Origin (0, 0) at top-left
- X increases eastward (right)
- Y increases southward (down)
- Scale: ~100x100 units per floor represents the full cross-shaped footprint
- Cross shape: North arm (top), South arm (bottom), East arm (right), 
               West arm (left), Center junction

Floor Structure:
- L1: Special asymmetrical layout (smaller, no full west arm)
- L2-L8: Full cross-shaped layout
- L9: Partial layout (west arm + center only)
"""

# Building-wide constants
BUILDING_ID = "69"
CROSS_WIDTH = 100
CROSS_HEIGHT = 100

# Define floor outlines (cross-shaped regions for each floor)
FLOOR_OUTLINES = {
    # Level 1: Asymmetrical - smaller footprint, irregular shape
    "1": {
        "name": "Level 1",
        "cross_type": "asymmetrical",
        "north_arm": {"x": 30, "y": 0, "w": 40, "h": 20},  # Contains 110 seminar room
        "center": {"x": 35, "y": 18, "w": 30, "h": 18},    # Utility cluster
        "south_arm": {"x": 20, "y": 35, "w": 60, "h": 20}, # Contains 105 bike storage
        "east_extension": {"x": 65, "y": 15, "w": 20, "h": 22},  # 111, 191
        "west_arm": None,  # No full west arm on L1
    },
    # Levels 2-8: Full cross-shaped layout
    "2": {
        "name": "Level 2 - Main Office/Lab Floor",
        "cross_type": "full_cross",
        "north_arm": {"x": 20, "y": 0, "w": 60, "h": 24},
        "east_arm": {"x": 70, "y": 24, "w": 26, "h": 50},
        "south_arm": {"x": 20, "y": 70, "w": 60, "h": 26},
        "west_arm": {"x": 0, "y": 24, "w": 20, "h": 50},
        "center_junction": {"x": 20, "y": 24, "w": 50, "h": 46},
        "corridor": {"y": 24, "height": 3},  # Horizontal corridor
    },
    "3": {
        "name": "Level 3 - Computing/Lab Floor",
        "cross_type": "full_cross",
        "north_arm": {"x": 20, "y": 0, "w": 60, "h": 24},
        "east_arm": {"x": 70, "y": 24, "w": 26, "h": 50},
        "south_arm": {"x": 20, "y": 70, "w": 60, "h": 26},
        "west_arm": {"x": 0, "y": 24, "w": 20, "h": 50},
        "center_junction": {"x": 20, "y": 24, "w": 50, "h": 46},
        "corridor": {"y": 24, "height": 3},
    },
    "4": {
        "name": "Level 4 - Teaching/Office Floor",
        "cross_type": "full_cross",
        "north_arm": {"x": 20, "y": 0, "w": 60, "h": 24},
        "east_arm": {"x": 70, "y": 24, "w": 26, "h": 50},
        "south_arm": {"x": 20, "y": 70, "w": 60, "h": 26},
        "west_arm": {"x": 0, "y": 24, "w": 20, "h": 50},
        "center_junction": {"x": 20, "y": 24, "w": 50, "h": 46},
        "corridor": {"y": 24, "height": 3},
    },
    "5": {
        "name": "Level 5 - Office/Meeting Floor",
        "cross_type": "full_cross",
        "north_arm": {"x": 20, "y": 0, "w": 60, "h": 24},
        "east_arm": {"x": 70, "y": 24, "w": 26, "h": 50},
        "south_arm": {"x": 20, "y": 70, "w": 60, "h": 26},
        "west_arm": {"x": 0, "y": 24, "w": 20, "h": 50},
        "center_junction": {"x": 20, "y": 24, "w": 50, "h": 46},
        "corridor": {"y": 24, "height": 3},
    },
    "6": {
        "name": "Level 6 - Research Staff Office Floor",
        "cross_type": "full_cross",
        "north_arm": {"x": 20, "y": 0, "w": 60, "h": 24},
        "east_arm": {"x": 70, "y": 24, "w": 26, "h": 50},
        "south_arm": {"x": 20, "y": 70, "w": 60, "h": 26},
        "west_arm": {"x": 0, "y": 24, "w": 20, "h": 50},
        "center_junction": {"x": 20, "y": 24, "w": 50, "h": 46},
        "corridor": {"y": 24, "height": 3},
    },
    "7": {
        "name": "Level 7 - Academic Staff Office Floor",
        "cross_type": "full_cross",
        "north_arm": {"x": 20, "y": 0, "w": 60, "h": 24},
        "east_arm": {"x": 70, "y": 24, "w": 26, "h": 50},
        "south_arm": {"x": 20, "y": 70, "w": 60, "h": 26},
        "west_arm": {"x": 0, "y": 24, "w": 20, "h": 50},
        "center_junction": {"x": 20, "y": 24, "w": 50, "h": 46},
        "corridor": {"y": 24, "height": 3},
    },
    "8": {
        "name": "Level 8 - Staff Office Floor",
        "cross_type": "full_cross",
        "north_arm": {"x": 20, "y": 0, "w": 60, "h": 24},
        "east_arm": {"x": 70, "y": 24, "w": 26, "h": 50},
        "south_arm": {"x": 20, "y": 70, "w": 60, "h": 26},
        "west_arm": {"x": 0, "y": 24, "w": 20, "h": 50},
        "center_junction": {"x": 20, "y": 24, "w": 50, "h": 46},
        "corridor": {"y": 24, "height": 3},
    },
    # Level 9: Partial layout
    "9": {
        "name": "Level 9 - Partial Floor",
        "cross_type": "partial",
        "west_arm": {"x": 0, "y": 30, "w": 20, "h": 40},
        "center_junction": {"x": 20, "y": 30, "w": 50, "h": 40},
        "corridor": {"y": 33, "height": 2},
    }
}

# Define stair and lift core positions (consistent across floors 2-9)
VERTICAL_CORES = {
    "stairs_298": {"x": 8, "y": 24, "w": 4, "h": 50},  # West side stairs
    "stairs_397": {"x": 8, "y": 24, "w": 4, "h": 50},  # Stairs continue up
    "lift_299": {"x": 12, "y": 24, "w": 4, "h": 50},   # West side lift
    "lift_399": {"x": 12, "y": 24, "w": 4, "h": 50},   # Lift continues up
}

# Room coordinate mappings for each floor
# Format: room_id: {"x": x, "y": y, "w": width, "h": height, "arm": "north|south|east|west|center"}

ROOM_COORDINATES = {
    "1": {  # Level 1
        # North arm - large seminar room
        "110": {"x": 35, "y": 4, "w": 30, "h": 14, "arm": "north", "label": "Seminar Room"},
        
        # Center utility cluster
        "109": {"x": 40, "y": 19, "w": 8, "h": 6, "arm": "center", "label": "Plant Room"},
        "108": {"x": 36, "y": 20, "w": 12, "h": 5, "arm": "center", "label": "Switch Room"},
        "107": {"x": 45, "y": 19, "w": 12, "h": 8, "arm": "center", "label": "Plant Room"},
        "106": {"x": 35, "y": 26, "w": 12, "h": 8, "arm": "center", "label": "Sub-Station"},
        
        # South arm - bike storage
        "105": {"x": 25, "y": 37, "w": 30, "h": 16, "arm": "south", "label": "Bicycle Storage"},
        
        # East extension
        "111": {"x": 68, "y": 18, "w": 15, "h": 10, "arm": "east", "label": "Plant Room"},
        "191": {"x": 70, "y": 30, "w": 12, "h": 8, "arm": "east", "label": "Covered Area"},
    },
    
    "2": {  # Level 2
        # North arm offices & seminar
        "207B": {"x": 50, "y": 4, "w": 10, "h": 6, "arm": "north", "label": "Office"},
        "207A": {"x": 62, "y": 4, "w": 10, "h": 6, "arm": "north", "label": "Office"},
        "207": {"x": 56, "y": 10, "w": 12, "h": 6, "arm": "north", "label": "Reception"},
        "206B": {"x": 40, "y": 6, "w": 12, "h": 8, "arm": "north", "label": "Meeting Room"},
        "206A": {"x": 40, "y": 14, "w": 12, "h": 8, "arm": "north", "label": "Meeting Room"},
        "206": {"x": 54, "y": 18, "w": 12, "h": 4, "arm": "north", "label": "Waiting Area"},
        
        # East arm - computing labs & offices
        "209": {"x": 72, "y": 28, "w": 20, "h": 14, "arm": "east", "label": "Computing Lab"},
        "208": {"x": 72, "y": 44, "w": 20, "h": 14, "arm": "east", "label": "Computing Lab"},
        
        # South arm - more labs & spaces
        "225": {"x": 30, "y": 72, "w": 12, "h": 10, "arm": "south", "label": "Mail Room"},
        
        # West arm - lift, stairs, utilities
        "299": {"x": 12, "y": 24, "w": 4, "h": 50, "arm": "west", "label": "Lift"},
        "298": {"x": 8, "y": 24, "w": 4, "h": 50, "arm": "west", "label": "Stairs"},
        
        # Center junction - circulation, utilities, risers
        "290": {"x": 25, "y": 28, "w": 15, "h": 8, "arm": "center", "label": "Circulation"},
        "295": {"x": 25, "y": 38, "w": 15, "h": 8, "arm": "center", "label": "Circulation"},
        "294": {"x": 38, "y": 35, "w": 12, "h": 10, "arm": "center", "label": "Circulation"},
        "297": {"x": 8, "y": 24, "w": 4, "h": 50, "arm": "center", "label": "Stairs"},
        "211": {"x": 28, "y": 50, "w": 8, "h": 6, "arm": "center", "label": "Electrical Riser"},
        "212": {"x": 38, "y": 50, "w": 8, "h": 6, "arm": "center", "label": "Comms Riser"},
        "213": {"x": 48, "y": 50, "w": 8, "h": 6, "arm": "center", "label": "Hydraulics Riser"},
        "296": {"x": 45, "y": 28, "w": 8, "h": 8, "arm": "center", "label": "Hand Sanitiser"},
        "207C": {"x": 45, "y": 38, "w": 12, "h": 6, "arm": "center", "label": "Kitchenette"},
        "210": {"x": 32, "y": 60, "w": 10, "h": 6, "arm": "center", "label": "Plant Room"},
    },
    
    "3": {  # Level 3
        # North arm - computing labs
        "316": {"x": 35, "y": 6, "w": 25, "h": 14, "arm": "north", "label": "Computing Lab"},
        "315": {"x": 62, "y": 6, "w": 12, "h": 14, "arm": "north", "label": "Computing Lab"},
        
        # East arm
        "304": {"x": 72, "y": 32, "w": 18, "h": 14, "arm": "east", "label": "Computing Lab"},
        "305": {"x": 72, "y": 48, "w": 18, "h": 14, "arm": "east", "label": "Computing Lab"},
        
        # West arm
        "399": {"x": 12, "y": 24, "w": 4, "h": 50, "arm": "west", "label": "Lift"},
        "398": {"x": 8, "y": 24, "w": 4, "h": 50, "arm": "west", "label": "Stairs"},
        
        # Center - circulation & utilities
        "330A": {"x": 28, "y": 50, "w": 8, "h": 6, "arm": "center", "label": "Electrical Riser"},
        "330": {"x": 36, "y": 50, "w": 10, "h": 6, "arm": "center", "label": "Plant Room"},
        "330B": {"x": 48, "y": 50, "w": 8, "h": 6, "arm": "center", "label": "Comms Riser"},
        "321A": {"x": 42, "y": 42, "w": 8, "h": 6, "arm": "center", "label": "Hydraulics Riser"},
        "322": {"x": 52, "y": 42, "w": 8, "h": 6, "arm": "center", "label": "Fire Riser"},
        "397": {"x": 8, "y": 24, "w": 4, "h": 50, "arm": "center", "label": "Stairs"},
        "395": {"x": 22, "y": 35, "w": 15, "h": 8, "arm": "center", "label": "Circulation"},
        "396": {"x": 45, "y": 28, "w": 8, "h": 8, "arm": "center", "label": "Circulation"},
        "331": {"x": 28, "y": 60, "w": 10, "h": 6, "arm": "center", "label": "Plant Room"},
    },
    
    "4": {  # Level 4
        # North arm - teaching & offices
        "416": {"x": 25, "y": 4, "w": 12, "h": 12, "arm": "north", "label": "Office"},
        "417": {"x": 40, "y": 4, "w": 12, "h": 12, "arm": "north", "label": "Office"},
        "415": {"x": 25, "y": 16, "w": 12, "h": 6, "arm": "north", "label": "Office"},
        "413": {"x": 40, "y": 16, "w": 12, "h": 6, "arm": "north", "label": "Staff Common Room"},
        "418": {"x": 56, "y": 8, "w": 20, "h": 14, "arm": "north", "label": "Large Office Space"},
        "412": {"x": 62, "y": 22, "w": 10, "h": 3, "arm": "north", "label": "Junction Room"},
        "414": {"x": 30, "y": 22, "w": 16, "h": 2, "arm": "north", "label": "Reception"},
        
        # East arm
        "492": {"x": 72, "y": 30, "w": 20, "h": 20, "arm": "east", "label": "Circulation/Lab Space"},
        "401": {"x": 75, "y": 55, "w": 18, "h": 12, "arm": "east", "label": "Collaborative Classroom"},
        
        # South arm - teaching spaces
        "407": {"x": 30, "y": 72, "w": 20, "h": 8, "arm": "south", "label": "Teaching Room"},
        "404": {"x": 52, "y": 72, "w": 14, "h": 8, "arm": "south", "label": "Teaching Room"},
        "493": {"x": 30, "y": 80, "w": 8, "h": 5, "arm": "south", "label": "Stairwell Landing"},
        "406": {"x": 30, "y": 86, "w": 20, "h": 8, "arm": "south", "label": "Teaching Room"},
        "405": {"x": 52, "y": 86, "w": 14, "h": 8, "arm": "south", "label": "Teaching Room"},
        
        # West arm
        "496": {"x": 3, "y": 28, "w": 14, "h": 8, "arm": "west", "label": "Circulation"},
        "408": {"x": 5, "y": 45, "w": 12, "h": 10, "arm": "west", "label": "Study Area"},
        "410": {"x": 5, "y": 58, "w": 12, "h": 10, "arm": "west", "label": "Study Area"},
        "499": {"x": 12, "y": 24, "w": 4, "h": 50, "arm": "west", "label": "Lift"},
        "498": {"x": 8, "y": 24, "w": 4, "h": 50, "arm": "west", "label": "Stairs"},
        
        # Center
        "419": {"x": 35, "y": 50, "w": 10, "h": 6, "arm": "center", "label": "Plant Room"},
        "420B": {"x": 48, "y": 42, "w": 8, "h": 6, "arm": "center", "label": "Hydraulics Riser"},
    },
    
    "5": {  # Level 5
        # North arm
        "520": {"x": 35, "y": 4, "w": 35, "h": 18, "arm": "north", "label": "Large Open Office"},
        
        # East arm - meeting rooms & hot desks
        "593": {"x": 73, "y": 27, "w": 18, "h": 6, "arm": "east", "label": "Circulation"},
        "503": {"x": 73, "y": 35, "w": 10, "h": 8, "arm": "east", "label": "Meeting Room"},
        "502": {"x": 83, "y": 35, "w": 10, "h": 8, "arm": "east", "label": "Hot Desk"},
        "501": {"x": 73, "y": 45, "w": 10, "h": 8, "arm": "east", "label": "Hot Desk"},
        "505": {"x": 73, "y": 56, "w": 10, "h": 8, "arm": "east", "label": "Meeting Room"},
        "504": {"x": 83, "y": 56, "w": 10, "h": 8, "arm": "east", "label": "Meeting Room"},
        
        # South arm
        "590": {"x": 30, "y": 72, "w": 35, "h": 20, "arm": "south", "label": "Large Teaching Space"},
        
        # West arm
        "599": {"x": 12, "y": 24, "w": 4, "h": 50, "arm": "west", "label": "Lift"},
        "598": {"x": 8, "y": 24, "w": 4, "h": 50, "arm": "west", "label": "Stairs"},
    },
    
    "6": {  # Level 6
        # North arm - meeting rooms
        "612": {"x": 35, "y": 4, "w": 30, "h": 18, "arm": "north", "label": "Open Plan Office"},
        
        # East arm
        "623": {"x": 72, "y": 28, "w": 20, "h": 16, "arm": "east", "label": "Office"},
        "604": {"x": 75, "y": 50, "w": 18, "h": 14, "arm": "east", "label": "Office"},
        
        # South arm
        "602": {"x": 30, "y": 72, "w": 16, "h": 8, "arm": "south", "label": "Meeting Room"},
        "618": {"x": 50, "y": 72, "w": 12, "h": 8, "arm": "south", "label": "Office"},
        
        # Center
        "608": {"x": 35, "y": 50, "w": 14, "h": 8, "arm": "center", "label": "Meeting Room"},
        "603": {"x": 50, "y": 50, "w": 12, "h": 8, "arm": "center", "label": "Resource Room"},
        "601": {"x": 50, "y": 38, "w": 12, "h": 8, "arm": "center", "label": "Staff Common Room"},
        
        # West arm
        "699": {"x": 12, "y": 24, "w": 4, "h": 50, "arm": "west", "label": "Lift"},
        "698": {"x": 8, "y": 24, "w": 4, "h": 50, "arm": "west", "label": "Stairs"},
    },
    
    "7": {  # Level 7
        # North arm - open plan offices
        "726": {"x": 35, "y": 4, "w": 30, "h": 18, "arm": "north", "label": "Open Plan Office"},
        "702": {"x": 68, "y": 8, "w": 14, "h": 14, "arm": "north", "label": "Office"},
        
        # East arm
        "707": {"x": 73, "y": 30, "w": 12, "h": 12, "arm": "east", "label": "Open Plan"},
        "706": {"x": 73, "y": 44, "w": 12, "h": 12, "arm": "east", "label": "Open Plan"},
        
        # North-east area
        "713": {"x": 73, "y": 10, "w": 12, "h": 10, "arm": "north", "label": "Open Plan"},
        
        # Center & junction
        "703": {"x": 40, "y": 50, "w": 12, "h": 10, "arm": "center", "label": "Office"},
        
        # West arm
        "799": {"x": 12, "y": 24, "w": 4, "h": 50, "arm": "west", "label": "Lift"},
        "798": {"x": 8, "y": 24, "w": 4, "h": 50, "arm": "west", "label": "Stairs"},
    },
    
    "8": {  # Level 8
        # North arm
        "812": {"x": 35, "y": 4, "w": 30, "h": 18, "arm": "north", "label": "Office Space"},
        
        # East arm
        "807": {"x": 73, "y": 30, "w": 20, "h": 36, "arm": "east", "label": "Open Plan Office"},
        
        # South arm
        "817": {"x": 30, "y": 72, "w": 20, "h": 20, "arm": "south", "label": "Dining Area"},
        
        # West arm
        "899": {"x": 12, "y": 24, "w": 4, "h": 50, "arm": "west", "label": "Lift"},
        "898": {"x": 8, "y": 24, "w": 4, "h": 50, "arm": "west", "label": "Stairs"},
    },
    
    "9": {  # Level 9 - Partial
        # West arm
        "999": {"x": 12, "y": 30, "w": 4, "h": 40, "arm": "west", "label": "Lift"},
        "998": {"x": 8, "y": 30, "w": 4, "h": 40, "arm": "west", "label": "Stairs"},
    }
}

# Helper function to get room info
def get_room_coordinates(floor, room_id):
    """Get coordinate data for a specific room."""
    if floor in ROOM_COORDINATES:
        return ROOM_COORDINATES[floor].get(room_id)
    return None

def get_floor_outline(floor):
    """Get the floor outline definition."""
    return FLOOR_OUTLINES.get(floor)

def get_all_room_coordinates(floor):
    """Get all room coordinates for a floor."""
    return ROOM_COORDINATES.get(floor, {})
