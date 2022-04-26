import math
from FibonacciHeap import FibonacciHeap
from Graph import Graph
from typing import List

# Reference: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Using_a_priority_queue
def FindPath(graph : Graph, from_node : int, to_node : int) -> List[int]:
    """Uses Dijkstra's algorithm to find a path from the node with index from_node to the node with index to_node on the graph."""
    node_count : int = len(graph.data)
    dist : List[float] = [math.inf for i in range(node_count)]
    prev : List[int] = [None for i in range(node_count)]
    queue_nodes = [None for i in range(node_count)]
    values_removed = []

    dist[from_node] = 0.0

    priority_queue = FibonacciHeap()

    for i in range(node_count):
        queue_nodes[i] = priority_queue.insert(dist[i], i)

    while priority_queue.total_nodes > 0:
        u = priority_queue.extract_min()

        if(u is None):
            break
        
        values_removed.append(u.value)
        
        for v in graph.neighbours(u.value):
            if(v in values_removed):
                continue

            alternate_path_through_u = dist[u.value] + graph.distance(u.value, v)
            if(alternate_path_through_u < dist[v]):
                dist[v] = alternate_path_through_u
                prev[v] = u.value
                priority_queue.decrease_key(queue_nodes[v], alternate_path_through_u)
        
        if u.value == to_node:
            break
    
    prev[from_node] = None

    if(prev[to_node] is None):
        return []

    path = []
    cur = to_node
    while cur != None:
        path.append(cur)
        cur = prev[cur]

    return path