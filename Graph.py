import math
from os import path
from typing import List
from Parser import Parse, ParseResults
from Edge import Edge
from Utility import Squared_Distance

GraphRepresentation = {"LIST": 0, "MATRIX": 1}

class Graph:
    """Represents a non-directed graph data structure, using either an adjacency list or an adjacency matrix."""
    representation : int = GraphRepresentation["LIST"]
    data = []

    def __init__(self, representation : int, data):
        self.representation = representation
        self.data = data

    def are_connected(self, a : int, b : int) -> bool:
        """Returns true if vertices of indices a and b are connected by an edge, and false otherwise."""
        if(self.representation == GraphRepresentation["LIST"]):
            return b in self.data[a]
        else:
            return self.data[a][b] != -1.0 and a != b

    def distance(self, a : int, b : int) -> float:
        """Returns the distance between vertices of indices a and b."""
        if(self.representation == GraphRepresentation["LIST"]):
            adjacency_list_for_a = self.data[a]
            for v in adjacency_list_for_a:
                if(v[0] == b):
                    return v[1]
            return -1.0
        else:
            return self.data[a][b]

    def neighbours(self, v : int) -> List[int]:
        """Returns a list with the indices of all the connected neighbouring vertices of the vertex with index v."""
        if(self.representation == GraphRepresentation["LIST"]):
            return self.data[v]
        else:
            res = []
            for i in range(len(self.data)):
                if(self.data[v][i] != -1.0 and i != v):
                    res.append(i)
            
            return res

def ParseIntoGraph(results : ParseResults, forcetype = -1) -> Graph:
    """Parses the result of reading the obj file into a graph."""
    edge_count = 0
    face_count = len(results.faces)
    
    # Finds Number of Edges in the Graph
    for edge in results.edges:
        n = len(results.edges[edge])
        if(n <= 1): continue
        edge_count += math.comb(n, 2)

    # Calculate density of graph
    graph_density = edge_count / (face_count ** 2)

    '''
    A float in python is represented by 64 bits, or 8 bytes. Then, we have that an adjacency matrix for n vertices (faces) requires 8(n^2) bytes for its representation.
    Alternatively, an adjacency list for m edges (connected face borders) needs to store 2 * m * (sizeof(integer) + sizeof(float)) = 2 * m * (8 + 8) = 32m bytes for its representation.
    Then, for 8(n^2) < 32m => n^2 < 4m => m/n^2 > 1/32  => graph_density > 1/32 is the case where an adjacency matrix is favourable.
    '''

    graph_type = GraphRepresentation["LIST"]
    
    if(graph_density > 1/32):
        graph_type = GraphRepresentation["MATRIX"]
    
    if(forcetype != -1):
        graph_type = forcetype

    data = []

    if(graph_type == GraphRepresentation["LIST"]):
        # Initialise data, data[face_index] holds a tuple of type (connected_face_index, distance) for each face the face with index face_index is connected to
        data = [[] for i in range(face_count)] 
        
        for edge in results.edges:
            # Get the list of the faces connected by this edge and the center of this edge.
            connected_faces = results.edges[edge]
            center = edge.get_edge_center(results)

            # If this edge connects no faces (that is, it does not lie in at least 2 faces), there is no need to consider it.
            if len(connected_faces) < 2:
                continue

            # We keep track of the face pairs which we have considered through this edge. This is kept edge-wise, since there might exist some face pairs which are connected by multiple edges, and we want to revisit them for each edge, since we want to hold the minimum distance through all of the connecting edges.
            considered_through_edge = []

            for face in connected_faces:
                for in_face in connected_faces:

                    # If both the faces are the same face or we have already inserted this data point, skip to the next iteration.
                    if(face.index == in_face.index or Edge(face.index, in_face.index) in considered_through_edge):
                        continue

                    # Calculate the squared distance between the faces through this edge.
                    sqr_distance = Squared_Distance(in_face.get_face_center(results), center) + Squared_Distance(center, face.get_face_center(results))
                    
                    index_in_adjacency = -1

                    for (i,adjacent) in enumerate(data[face.index]):
                        if adjacent[0] == in_face.index:
                            index_in_adjacency = i
                            break
                    
                    if index_in_adjacency == -1:
                        # If a record for in_face does not already exist in face's adjacency list (and vice versa), we record it.
                        data[face.index].append((in_face.index, sqr_distance))
                        data[in_face.index].append((face.index, sqr_distance))
                    else:
                        # If it already exists, we calculate the distance through this edge and set the distance between the faces to the minimum of the old distance and the new distance.
                        current_distance = data[face.index][index_in_adjacency][1]
                        data[face.index][index_in_adjacency] = (in_face.index, min(current_distance, sqr_distance))

                        inverse_index = -1

                        for (i, adjacent) in enumerate(data[in_face.index]):
                            if(adjacent[0] == face.index):
                                inverse_index = i
                                break
                        
                        if(inverse_index == -1):
                            # in_face exists in face's adjacency list, but not vice versa. Something has gone incredibly wrong.
                            print("Something went horribly wrong while parsing")
                            exit(1)

                        data[in_face.index][inverse_index] = (face.index, min(current_distance, sqr_distance))

                    # Finally, we add the face pair to the considered through edge list, so that we do not calculate the distance between them through this edge again. We use the Edge datastructure since this should be an unordered pair.
                    considered_through_edge.append(Edge(face.index, in_face.index)) 
    else:
        # Initialise data, the adjacency matrix format holds an 2-dimensional array of size n x n, where n is the number of faces. Here, data[i][j] = data[j][i], hold the distance between the faces with indices i and j, if they are connected, and -1 otherwise.
        data = [[-1.0 for j in range(face_count)] for i in range(face_count)]

        # The logic for the main loop is much the same as case 1, with differences made for the different data structure.
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

if __name__ == "__main__":
    file_path = "examples/flap.obj"
    
    if(not path.exists(file_path)):
        print(f"File {path.abspath(file_path)} not found.")
        exit(1)

    results = None
    with open(file_path, "r") as f:
        results = Parse(f)

    graph = ParseIntoGraph(results)
    print(graph.data)