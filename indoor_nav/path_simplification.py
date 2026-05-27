import math
import re
from typing import List, Optional, Set
from .models import Node


# ── Geometry helpers ──────────────────────────────────────────────────────────

def _haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Distance in metres between two lat/lng points."""
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi  = math.radians(lat2 - lat1)
    dlng  = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlng / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _bearing(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Compass bearing 0-360° (clockwise from north)."""
    dlng = lng2 - lng1
    y = math.sin(math.radians(dlng)) * math.cos(math.radians(lat2))
    x = (math.cos(math.radians(lat1)) * math.sin(math.radians(lat2))
         - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.cos(math.radians(dlng)))
    return (math.degrees(math.atan2(y, x)) + 360) % 360


def _angle_diff(a1: float, a2: float) -> float:
    """Minimum angular difference between two bearings (0-180)."""
    d = abs(a2 - a1)
    return min(d, 360 - d)


# ── Node property helpers ─────────────────────────────────────────────────────

def _building_key(node: Node) -> str:
    raw = (node.building or '').strip().lower()
    m = re.search(r'\b(\d+)\b', raw)
    return m.group(1) if m else raw


def _building_label(node: Node) -> str:
    raw = (node.building or 'Unknown building').strip()
    # Bare number → prefix with "Building"
    if raw.isdigit():
        return f'Building {raw}'
    return raw


def _floor_key(node: Node) -> str:
    return (node.floor or '').strip().lower()


def _has_coords(node: Node) -> bool:
    return bool(node.lat and node.lng)


# ── Segment distance / formatting ─────────────────────────────────────────────

def _segment_distance(nodes: List[Node], start: int, end: int) -> Optional[float]:
    total, counted = 0.0, 0
    for i in range(start, end):
        n1, n2 = nodes[i], nodes[i + 1]
        if _has_coords(n1) and _has_coords(n2):
            total += _haversine(n1.lat, n1.lng, n2.lat, n2.lng)
            counted += 1
    return total if counted else None


def _format_dist(metres: Optional[float]) -> str:
    if metres is None:
        return ''
    return f'~{round(metres)}m' if metres < 5 else f'~{round(metres / 5) * 5}m'


def _seg_bearing(start: Node, end: Node) -> Optional[float]:
    if _has_coords(start) and _has_coords(end):
        return _bearing(start.lat, start.lng, end.lat, end.lng)
    return None


# ── Turn direction ─────────────────────────────────────────────────────────────

def _turn_direction(prev_bearing: Optional[float], curr_bearing: Optional[float]) -> str:
    if prev_bearing is None or curr_bearing is None:
        return 'straight'
    diff = curr_bearing - prev_bearing
    while diff >  180: diff -= 360
    while diff < -180: diff += 360
    if abs(diff) < 15:
        return 'straight'
    if diff > 0:
        return 'right (sharp)' if diff > 100 else 'right'
    return 'left (sharp)' if diff < -100 else 'left'


# ── Break-point collection ────────────────────────────────────────────────────

def _edge_bearing(n_cur: Node, n_next: Node) -> Optional[float]:
    """Bearing of a single graph edge, or None when coords are missing."""
    if _has_coords(n_cur) and _has_coords(n_next):
        return _bearing(n_cur.lat, n_cur.lng, n_next.lat, n_next.lng)
    return None


def _is_context_change(n_cur: Node, n_next: Node) -> bool:
    """True when consecutive nodes cross a building or floor boundary."""
    return (_building_key(n_cur) != _building_key(n_next)
            or _floor_key(n_cur) != _floor_key(n_next))


def _is_direction_change(seg_bearing: Optional[float], edge_b: Optional[float],
                          threshold: float) -> bool:
    """True when the edge bearing deviates from the current segment bearing."""
    if edge_b is None or seg_bearing is None:
        return False
    return _angle_diff(seg_bearing, edge_b) > threshold


def _collect_break_points(nodes: List[Node], angle_threshold: float) -> Set[int]:
    """
    Return indices where a new segment should start.
    Hard breaks at building / floor transitions; soft breaks on direction changes.
    """
    breaks: Set[int] = {0, len(nodes) - 1}
    seg_bearing: Optional[float] = None

    for i in range(len(nodes) - 1):
        n_cur, n_next = nodes[i], nodes[i + 1]
        edge_b = _edge_bearing(n_cur, n_next)
        if seg_bearing is None:
            seg_bearing = edge_b

        if (_is_context_change(n_cur, n_next)
                or _is_direction_change(seg_bearing, edge_b, angle_threshold)):
            breaks.add(i + 1)
            seg_bearing = edge_b
        else:
            seg_bearing = edge_b or seg_bearing

    return breaks


# ── Description builders ──────────────────────────────────────────────────────

def _notable_rooms(inter: List[Node]) -> List[str]:
    return [n.label for n in inter
            if n.type and n.type.lower() not in ('corridor',)]


def _desc_first_segment(end_node: Node, inter: List[Node], dist_str: str,
                         bld_change: bool) -> str:
    dist_part = f' ({dist_str})' if dist_str else ''
    if bld_change and inter:
        via = inter[0].label          # first intermediate node (e.g. 395 - Circulation Space)
        return (f'Head through {via}, then enter {_building_label(end_node)}'
                f' to reach {end_node.label}{dist_part}')
    if bld_change:
        return f'Enter {_building_label(end_node)}, walk to {end_node.label}{dist_part}'
    return f'Head towards {end_node.label}{dist_part}'


def _desc_transition_segment(start_node: Node, end_node: Node,
                              turn: str, dist_str: str, flr_change: bool) -> str:
    dist_part = f' ({dist_str})' if dist_str else ''
    if flr_change:
        action = 'Take the stairs/lift'
        return (f'{action} from Floor {start_node.floor} to Floor {end_node.floor}'
                f', entering {_building_label(end_node)}{dist_part}')
    turn_part = '' if turn == 'straight' else f', turn {turn}'
    return f'Enter {_building_label(end_node)}{turn_part}, walk to {end_node.label}{dist_part}'


def _desc_regular_segment(end_node: Node, inter: List[Node],
                           turn: str, dist_str: str) -> str:
    dist_part = f' ({dist_str})' if dist_str else ''
    turn_verb = 'Continue straight' if turn == 'straight' else f'Turn {turn}'
    notable = _notable_rooms(inter)
    if notable:
        rooms_str = ', '.join(notable[:3])
        return f'{turn_verb} through {rooms_str} to {end_node.label}{dist_part}'
    return f'{turn_verb} to {end_node.label}{dist_part}'


def _make_description(start_node: Node, end_node: Node, inter: List[Node],
                       turn: str, dist_str: str, is_first: bool) -> str:
    bld_change = _building_key(start_node) != _building_key(end_node)
    flr_change = _floor_key(start_node)    != _floor_key(end_node)

    if is_first:
        return _desc_first_segment(end_node, inter, dist_str, bld_change)
    if bld_change or flr_change:
        return _desc_transition_segment(start_node, end_node, turn, dist_str, flr_change)
    return _desc_regular_segment(end_node, inter, turn, dist_str)


# ── Public API ────────────────────────────────────────────────────────────────

def simplify_path(nodes: List[Node], angle_threshold: float = 15.0) -> List[dict]:
    """
    Convert a raw node list into human-readable navigation segments.

    Hard breaks at every building / floor transition ensure each leg has a
    clear context even when the graph is sparse.  Soft breaks trigger on
    bearing changes larger than *angle_threshold* degrees.
    """
    if not nodes:
        return []
    if len(nodes) == 1:
        return [{
            'segment_index': 1, 'start_node': nodes[0], 'end_node': nodes[0],
            'intermediate_nodes': [], 'turn_direction': 'straight',
            'description': f'You are already at {nodes[0].label}', 'distance_m': None,
        }]

    sorted_breaks = sorted(_collect_break_points(nodes, angle_threshold))
    segments: List[dict] = []
    prev_bear: Optional[float] = None

    for k in range(len(sorted_breaks) - 1):
        s, e = sorted_breaks[k], sorted_breaks[k + 1]
        start_node = nodes[s]
        end_node   = nodes[e]
        inter      = nodes[s + 1:e]

        bear     = _seg_bearing(start_node, end_node)
        turn     = _turn_direction(prev_bear, bear)
        dist     = _segment_distance(nodes, s, e)
        dist_str = _format_dist(dist)
        desc     = _make_description(start_node, end_node, inter, turn, dist_str, k == 0)

        segments.append({
            'segment_index':      k + 1,
            'start_node':         start_node,
            'end_node':           end_node,
            'intermediate_nodes': inter,
            'turn_direction':     turn,
            'bearing':            bear,
            'distance_m':         dist,
            'description':        desc,
        })
        prev_bear = bear

    return segments


def format_directions(segments: List[dict], include_node_details: bool = False) -> str:
    lines = []
    for seg in segments:
        desc = seg['description']
        if include_node_details:
            desc += f" ({seg['start_node'].building} Floor {seg['start_node'].floor})"
        lines.append(f"{seg['segment_index']}. {desc}")
    return '\n'.join(lines)
