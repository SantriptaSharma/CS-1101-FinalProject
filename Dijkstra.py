import math
from FibonacciHeap import FibonacciHeap
from Graph import Graph
from typing import List

# Reference: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Using_a_priority_queue
def FindPath(graph : Graph, from_node : int, to_node : int) -> List[int]:
    """Uses Dijkstra's algorithm to find a path from the node with index from_node to the node with index to_node on the graph."""
    node_count = len(graph.data)
    dist = [math.inf for i in range(node_count)]
    prev = [None for i in range(node_count)]
    queue_nodes = [None for i in range(node_count)]

    dist[from_node] = 0

    priority_queue = FibonacciHeap()

    for i in range(node_count):
        queue_nodes[i] = priority_queue.insert(dist[i], i)

    while priority_queue.min_node is not None and priority_queue.total_nodes > 0:
        u = priority_queue.extract_min()
        for v in graph.neighbours(u.value):
            alternate_path_through_u = dist[u.value] + graph.distance(u.value, v)
            if(alternate_path_through_u < dist[v]):
                dist[v] = alternate_path_through_u
                prev[v] = u.value
                priority_queue.decrease_key(queue_nodes[v], alternate_path_through_u)
    
    prev[from_node] = None

    path = []
    cur = to_node
    while cur != None:
        path.append(cur)
        cur = prev[cur]

    return path