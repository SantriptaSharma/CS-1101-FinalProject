from typing import List
from Utility import Add_Positions, Scale_Positions

class FaceVertex:
    vert = -1
    tex = -1
    norm = -1

    def __init__(self, vertex : int, texture : int, normal : int):
        self.vert = vertex
        self.tex = texture
        self.norm = normal

class Face:
    index : int = -1
    verts : List[FaceVertex] = []

    def get_face_center(self, results):
        positions = []
        for v in self.verts:
            positions.append(results.verts[v.vert])
        
        summed = (0.0, 0.0, 0.0)
        for p in positions:
            summed = Add_Positions(summed, p)

        n = len(positions)

        return Scale_Positions(summed, 1/n)

    def __init__(self, vertices : List[FaceVertex], index : int):
        self.verts = vertices
        self.index = index

    def __repr__(self):
        return str(self)

    def __str__(self):
        out = ["("]
        for v in self.verts:
            repr = f"{v.vert}/{v.tex}/{v.norm}"
            repr = repr.replace("-1", "")
            out.append(repr)
            out.append(", ")
        out.pop()
        out.append(")")
        return "".join(out)
