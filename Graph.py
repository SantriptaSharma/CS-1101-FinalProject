import math
from typing import List
from Parser import ParseResults
from Edge import Edge
from Utility import Squared_Distance

GraphRepresentation = {"LIST": 0, "MATRIX": 1}

class Graph:
    representation : int = GraphRepresentation["LIST"]

    data = []

    def __init__(self, representation : int, data):
        self.representation = representation
        self.data = data

    def are_connected(self, a : int, b : int) -> bool:
        if(self.representation == GraphRepresentation["LIST"]):
            return b in self.data[a]
        else:
            return self.data[a][b] != -1.0

    def distance(self, a : int, b : int) -> float:
        if(self.representation == GraphRepresentation["LIST"]):
            adjacency_list_for_a = self.data[a]
            for v in adjacency_list_for_a:
                if(v[0] == b):
                    return v[1]
            return -1.0
        else:
            return self.data[a][b]

    def neighbours(self, v : int) -> List[int]:
        if(self.representation == GraphRepresentation["LIST"]):
            return self.data[v]
        else:
            res = []
            for i in range(len(self.data)):
                if(self.data[v][i] != -1.0 and i != v):
                    res.append(i)
            
            return res

def ParseIntoGraph(results : ParseResults, forcetype = -1) -> Graph:
    edge_count = 0
    face_count = len(results.faces)
    
    # Finds Number of Edges in the Graph
    for edge in results.edges:
        n = len(results.edges[edge])
        if(n <= 1): continue
        edge_count += math.comb(n, 2)

    graph_density = edge_count / (face_count ** 2)

    '''
    A float in python is represented by 64 bits, or 8 bytes. Then, we have that an adjacency matrix for n vertices (faces) requires 8(n^2) bytes for its representation.
    Alternatively, an adjacency list for m edges (connected face borders) needs to store 2 * m * (sizeof(integer) + sizeof(float)) = 2 * m * (8 + 8) = 32m bytes for its representation.
    Then, for 8(n^2) < 32m => n^2 < 4m => m/n^2 > 1/32 
    '''

    graph_type = GraphRepresentation["LIST"]
    
    if(graph_density > 1/32):
        graph_type = GraphRepresentation["MATRIX"]
    
    if(forcetype != -1):
        graph_type = forcetype

    print(f"Graph Type: {graph_type}")

    data = []

    if(graph_type == GraphRepresentation["LIST"]):
        data = [[] for i in range(face_count)] 
        for edge in results.edges:
            connected_faces = results.edges[edge]
            center = edge.get_edge_center(results)

            if len(connected_faces) < 2:
                continue

            considered_through_edge = []

            for face in connected_faces:
                for in_face in connected_faces:
                    if(face.index == in_face.index or Edge(face.index, in_face.index) in considered_through_edge):
                        continue

                    sqr_distance = Squared_Distance(in_face.get_face_center(results), center) + Squared_Distance(center, face.get_face_center(results))
                    
                    index_in_adjacency = -1

                    for (i,adjacent) in enumerate(data[face.index]):
                        if adjacent[0] == in_face.index:
                            index_in_adjacency = i
                            break
                    
                    if index_in_adjacency == -1:
                        data[face.index].append((in_face.index, sqr_distance))
                        data[in_face.index].append((face.index, sqr_distance))
                    else:
                        current_distance = data[face.index][index_in_adjacency][1]
                        data[face.index][index_in_adjacency] = (in_face.index, min(current_distance, sqr_distance))

                        inverse_index = -1

                        for (i, adjacent) in enumerate(data[in_face.index]):
                            if(adjacent[0] == face.index):
                                inverse_index = i
                                break
                        
                        if(inverse_index == -1):
                            print("Something went horribly wrong while parsing")
                            exit(1)

                        data[in_face.index][inverse_index] = (face.index, min(current_distance, sqr_distance))

                    considered_through_edge.append(Edge(face.index, in_face.index)) 
    else:
        data = [[-1.0 for j in range(face_count)] for i in range(face_count)]

        for edge in results.edges:
            connected_faces = results.edges[edge]
            center = edge.get_edge_center(results)
            if len(connected_faces) < 2:
                continue

            considered_through_edge = []

            for face in connected_faces:
                for in_face in connected_faces:
                    if(face.index == in_face.index or Edge(face.index, in_face.index) in considered_through_edge):
                        continue

                    sqr_distance = Squared_Distance(in_face.get_face_center(results), center) + Squared_Distance(center, face.get_face_center(results))
            
                    considered_through_edge.append(Edge(face.index, in_face.index))

                    if(data[face.index][in_face.index] == -1):
                        data[face.index][in_face.index] = sqr_distance
                        data[in_face.index][face.index] = sqr_distance
                    else:
                        c_val = data[face.index][in_face.index]
                        n_val = min(c_val, sqr_distance)

                        if(n_val == c_val): continue

                        data[face.index][in_face.index] = n_val
                        data[in_face.index][face.index] = n_val
                
                data[face.index][face.index] = 0.0

    return Graph(graph_type, data)