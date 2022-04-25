import math
from FibonacciHeap import Heap
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

    priority_queue = Heap()

    for i in range(node_count):
        queue_nodes[i] = priority_queue.add_with_priority(dist[i], i)

    while priority_queue.n != 0:
        u = priority_queue.extract_min()
        for v in graph.neighbours(u.val):
            alternate_path_through_u = dist[u.val] + graph.distance(u.val, v)
            if(alternate_path_through_u < dist[v]):
                dist[v] = alternate_path_through_u
                prev[v] = u.val
                priority_queue.decrease_key(queue_nodes[v], alternate_path_through_u)
    
    prev[from_node] = None

    path = []
    cur = to_node
    while cur != None:
        path.append(cur)
        cur = prev[cur]

    return path