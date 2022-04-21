class Edge(tuple):
    def __new__(self, a, b):
        return tuple.__new__(Edge, (a,b))
    
    # Unordered Hash
    def __hash__(self) -> int:
        return super().__hash__() + hash((self[1], self[0]))

    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __ne__(self, other):
        return not self.__eq__(self, other)