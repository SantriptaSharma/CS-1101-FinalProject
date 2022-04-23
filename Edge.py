from Utility import Add_Positions, Scale_Positions

class Edge(tuple):
    """Represents an unordered pair of elements. Used for edges since an edge between vertices a and b is the same as an edge between vertices b and a."""

    center = 0

    def get_edge_center(self, results):
        """Calculates and returns the center of this edge in 3D space. Uses a cache if possible."""
        if(self.center != 0):
            return self.center
        
        positions = [results.verts[self[0]], results.verts[self[1]]]
        
        summed = (0.0, 0.0, 0.0)
        for p in positions:
            summed = Add_Positions(summed, p)

        self.center = Scale_Positions(summed, 1/2)
        return self.center

    def __new__(self, a, b):
        self.center = 0
        return tuple.__new__(Edge, (a,b))
    
    # Unordered Hash
    def __hash__(self) -> int:
        return super().__hash__() + hash((self[1], self[0]))

    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __ne__(self, other):
        return not self.__eq__(self, other)