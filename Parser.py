from io import TextIOWrapper
from os import path
from typing import Dict, List, Tuple
from Edge import Edge
from Face import Face, FaceVertex

class ParseResults:
    global_props : List[str] = []
    object_props : List[str] = []
    verts : List[Tuple[float,float,float]] = []
    norms : List[Tuple[float,float,float]] = []
    texs  : List[Tuple[float,float]] = []
    faces : List[Face] = []
    edges : Dict[Edge, List[Face]] = {}

    def display(self):
        print("PARSE RESULTS")
        print("Globals")
        print(self.global_props)
        print()
        print("Object Properties")
        print(self.object_props)
        print()
        print("Vertices")
        print(self.verts)
        print()
        print("Texture Coordinates")
        print(self.texs)
        print()
        print("Normals")
        print(self.norms)
        print()
        print("Faces")
        print(self.faces)
        print()
        print("Edges")
        print(self.edges)
        print()

    def __init__(self):
        self.global_props = []
        self.object_props = []
        self.verts = []
        self.norms = []
        self.texs = []
        self.faces = []
        self.edges = {}

def ConsumeLine(results : ParseResults, tokens : List[str], in_object : bool):
    if(in_object):
        results.object_props.append(" ".join(tokens))
    else:
        results.global_props.append(" ".join(tokens))

def ConsumeVertex(results : ParseResults, tokens : List[str]):
    if(len(tokens) != 4):
        print("Vertex Coordinates Cannot be n-dimensional (n>3). Exiting.")
        exit(1)

    results.verts.append(tuple([float(token) for token in tokens[1:]]))

def ConsumeTexture(results : ParseResults, tokens : List[str]):
    if(len(tokens) != 3):
        print("Texture Coordinates Cannot be n-dimensional (n>2). Exiting.")
        exit(1)
        
    results.texs.append(tuple([float(token) for token in tokens[1:]]))

def ConsumeNormal(results: ParseResults, tokens : List[str]):
    if(len(tokens) != 4):
        print("Vertex Normals Cannot be n-dimensional (n>3). Exiting.")
        exit(1)

    results.norms.append(tuple([float(token) for token in tokens[1:]]))

def ConsumeFace(results: ParseResults, tokens : List[str]):
    verts : List[FaceVertex] = []
    edges : List[Edge] = []

    n = len(tokens)
    for i in range(1, n):
        vert = tokens[i]
        if("/" not in vert):
            vert = f"{vert}//"
        vert_data = [(-1 if i == "" else int(i)-1) for i in vert.split("/")]

        if(vert_data[0] == -1):
            print("Vertex Position Must Be Specified. Exiting.")
            exit(1)
        
        verts.append(FaceVertex(vert_data[0], vert_data[1], vert_data[2]))
        
        next_vert_index = int(tokens[1].split("/")[0])
        if(i != n-1):
            next_vert_index = int(tokens[i+1].split("/")[0])-1
        
        edges.append(Edge(vert_data[0], next_vert_index))

    face_index = len(results.faces)
    this_face = Face(verts, face_index)
    
    for edge in edges:
        if(edge in results.edges):
            results.edges[edge].append(this_face)
        else:
            results.edges[edge] = [this_face]
    
    results.faces.append(this_face)

function_table = {"v": ConsumeVertex, "vt": ConsumeTexture, "vn": ConsumeNormal, "f": ConsumeFace}

def Parse(wavefront : TextIOWrapper) -> ParseResults:
    result = ParseResults()
    in_object = False
    for line in wavefront.readlines():
        tokens = line.split(" ")
        
        key = tokens[0]

        if(in_object and key == "o"):
            print("Only One Object is Supported, Skipping any Further Objects.")
            return result

        if(not in_object and key == "o"):
            in_object = True

        if(key in function_table):
            function_table[key](result, tokens)
        else:
            ConsumeLine(result, tokens, in_object)
    
    return result

if __name__ == "__main__":
    file_path = "examples/flap.obj"
    
    if(not path.exists(file_path)):
        print(f"File {path.abspath(file_path)} not found.")
        exit(1)

    results = None
    with open(file_path, "r") as f:
        results = Parse(f)
    
    results.display()