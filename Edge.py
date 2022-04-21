from Utility import Add_Positions, Scale_Positions

class Edge(tuple):
    def get_edge_center(self, results):
        positions = [results.verts[self[0]], results.verts[self[1]]]
        
        summed = (0.0, 0.0, 0.0)
        for p in positions:
            summed = Add_Positions(summed, p)

        return Scale_Positions(summed, 1/2)

    def __new__(self, a, b):
        return tuple.__new__(Edge, (a,b))
    
    # Unordered Hash
    def __hash__(self) -> int:
        return super().__hash__() + hash((self[1], self[0]))

    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __ne__(self, other):
        return not self.__eq__(self, other)