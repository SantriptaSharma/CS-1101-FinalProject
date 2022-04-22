from Utility import Add_Positions, Scale_Positions

class Edge(tuple):
    center = -32

    def get_edge_center(self, results):
        if(self.center != -32):
            return self.center
        
        positions = [results.verts[self[0]], results.verts[self[1]]]
        
        summed = (0.0, 0.0, 0.0)
        for p in positions:
            summed = Add_Positions(summed, p)

        self.center = Scale_Positions(summed, 1/2)
        return self.center

    def __new__(self, a, b):
        self.center = -32
        return tuple.__new__(Edge, (a,b))
    
    # Unordered Hash
    def __hash__(self) -> int:
        return super().__hash__() + hash((self[1], self[0]))

    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __ne__(self, other):
        return not self.__eq__(self, other)