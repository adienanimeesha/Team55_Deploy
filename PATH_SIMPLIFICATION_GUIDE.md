# Path Simplification Feature

## Overview
Automatically compress long corridor paths into simplified, human-readable instructions by detecting collinear segments.

**Before:** "14 steps" listing every room passed through
**After:** "Go northeast through rooms 212, 211, 210 until you reach 208"

## How It Works

### 1. Bearing Calculation
For each pair of consecutive nodes, calculate the compass bearing (0-360°):
```
Bearing = direction from north, clockwise
Example: 45° = Northeast, 180° = South
```

### 2. Direction Change Detection
When the bearing changes by more than the **angle threshold** (default 15°), a new segment starts:
```
Nodes 1→2→3→4 with bearings [45°, 48°, 52°, 120°]
  Segments: [1→2→3→4 continue], [4→... new segment]
  (48-45=3° < 15°, 52-48=4° < 15°, but 120-52=68° > 15°)
```

### 3. Segment Description
Each segment is described as:
```
"Go [DIRECTION] [straight|through rooms] until you reach [END ROOM]"
```

## Files Modified

### New Files
- **`indoor_nav/path_simplification.py`** - Main algorithm
- **`path_simplification_demo.py`** - Test/demo script

### Modified Files
- **`maps/views.py`** - Calls simplification, passes to template
- **`maps/templates/maps/home.html`** - Displays simplified segments

## Usage

### In Views
```python
from indoor_nav.path_simplification import simplify_path, format_directions

# Get path from pathfinding
path, _ = dijkstra(start_id, end_id)

# Simplify it
simplified_segments = simplify_path(path, angle_threshold=15.0)

# Format for display
human_readable = format_directions(simplified_segments, include_node_details=True)
```

### In Templates
```django
{% if simplified_segments %}
    {% for segment in simplified_segments %}
        <div class="direction-step">
            <div class="step-num">{{ forloop.counter }}</div>
            <div>{{ segment.description }}</div>
            <div>{{ segment.direction_name }} · {{ segment.intermediate_nodes|length }} locations</div>
        </div>
    {% endfor %}
{% endif %}
```

## Customization

### Adjust Angle Threshold
Smaller threshold = more segments (more detailed)
Larger threshold = fewer segments (less detailed)

```python
# More detailed (8° threshold)
simplified = simplify_path(path, angle_threshold=8.0)

# Less detailed (25° threshold)
simplified = simplify_path(path, angle_threshold=25.0)
```

### Filter Intermediate Node Types
By default, "corridor" type nodes are excluded from the description. Modify in `_create_segment()`:

```python
# Only show rooms, exclude stairs/corridors/elevators
intermediate_labels = [
    n.label for n in intermediate_nodes 
    if n.type in ['room']  # Adjust as needed
]
```

### Change Compass Directions
Modify the `directions` list in `_create_segment()` to use different labels:
```python
directions = ['North', 'NNE', 'NE', ...] # 16-point compass
# Or simpler: ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'] # 8-point
```

## Performance

- **Bearing calculation**: O(n) where n = path length
- **Grouping**: Single pass O(n)
- **Overall**: Fast, negligible overhead

Example: 14-step path simplified in <1ms

## Testing

Run the demo script:
```bash
python manage.py shell < path_simplification_demo.py
```

Expected output:
```
Full path has 15 nodes

SIMPLIFIED PATH:
Segment 1: Go northeast straight through rooms 212, 211, 210...
Segment 2: Go east up the stairs to 698...
...

COMPRESSION RATIO: 5.0x (15 steps → 3 instructions)
```

## Edge Cases Handled

1. **Short paths** (< 3 nodes) - Returned as-is
2. **No direction change** - All nodes in one segment
3. **Nodes without coordinates** - Skipped in bearing calculations
4. **Same location nodes** - Handled gracefully
5. **Collinear nodes** - Correctly grouped together

## Future Enhancements

1. **Turn instructions** - "Turn right at 698"
2. **Distance estimation** - "Walk about 50 meters through..."
3. **Floor changes** - Special handling for stairs/elevators
4. **Landmark awareness** - "Pass the coffee shop" (if POIs added)
5. **Natural language** - "Head towards Building 62"
