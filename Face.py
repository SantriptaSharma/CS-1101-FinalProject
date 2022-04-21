from typing import List

class FaceVertex:
    vert = -1
    tex = -1
    norm = -1

    def __init__(self, vertex : int, texture : int, normal : int):
        self.vert = vertex
        self.tex = texture
        self.norm = normal

class Face:
    verts = [FaceVertex]

    def __init__(self, vertices : List[FaceVertex]):
        self.verts = vertices

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
