from io import TextIOWrapper
from typing import List
from Parser import ParseResults

def OutputPathAsWavefront(graph_path : List[int], out_file : TextIOWrapper, context : ParseResults):
    vertices_wanted = []
    textures_wanted = []
    normals_wanted = []
    vmap = {}
    tmap = {}
    nmap = {}

    for face_index in graph_path:
        for v in context.faces[face_index].verts:
            if v.vert not in vertices_wanted:
                vmap[v.vert] = len(vertices_wanted)
                vertices_wanted.append(v.vert)
            
            if v.tex != -1 and v.tex not in textures_wanted:
                tmap[v.tex] = len(textures_wanted)
                textures_wanted.append(v.tex)
            
            if v.norm != -1 and v.norm not in normals_wanted:
                nmap[v.norm] = len(normals_wanted)
                normals_wanted.append(v.norm)

    out_file.write("".join(context.global_props))
    name_string = "o " + context.object_props[0].removeprefix("o ").removesuffix("\n") + f"_Path_From_{graph_path[len(graph_path)-1]}_to_{graph_path[0]}\n"
    out_file.write(name_string)
    context.object_props.pop(0)
    out_file.write("".join(context.object_props))

    for v in vertices_wanted:
        vert = context.verts[v]
        out_file.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
    
    for vt in textures_wanted:
        tex = context.texs[vt]
        out_file.write(f"vt {tex[0]} {tex[1]}\n")

    for vn in normals_wanted:
        norm = context.norms[vn]
        out_file.write(f"vn {norm[0]} {norm[1]} {norm[2]}\n")
    
    for f in graph_path:
        face = context.faces[f]
        out_file.write("f")

        for v in face.verts:
            out_file.write(" ")
            nv = vmap[v.vert]
            nt = tmap[v.tex]
            nn = nmap[v.norm]
            out_file.write(f"{nv + 1}/{nt + 1 if nt != -1 else ''}/{nn + 1 if nn != -1 else ''}")
        
        out_file.write("\n")