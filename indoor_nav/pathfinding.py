import heapq
from .models import Node, Edge


def build_graph():
    graph = {}
    for node in Node.objects.all():
        graph[node.id] = []
    for edge in Edge.objects.select_related('from_node', 'to_node'):
        graph[edge.from_node_id].append((edge.to_node_id, edge.weight))
        graph[edge.to_node_id].append((edge.from_node_id, edge.weight))
    return graph


def dijkstra(start_id, end_id):
    graph = build_graph()

    if start_id not in graph or end_id not in graph:
        return None, None

    distances = {node: float('inf') for node in graph}
    distances[start_id] = 0
    previous = dict.fromkeys(graph)
    heap = [(0, start_id)]

    while heap:
        current_dist, current = heapq.heappop(heap)

        if current == end_id:
            break

        if current_dist > distances[current]:
            continue

        for neighbour, weight in graph[current]:
            dist = current_dist + weight
            if dist < distances[neighbour]:
                distances[neighbour] = dist
                previous[neighbour] = current
                heapq.heappush(heap, (dist, neighbour))

    if distances[end_id] == float('inf'):
        return None, None

    path = []
    current = end_id
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    nodes = {n.id: n for n in Node.objects.filter(id__in=path)}
    return [nodes[id] for id in path], distances[end_id]