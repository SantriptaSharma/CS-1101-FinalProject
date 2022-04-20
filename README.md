# PolyTraverse
### Goal
To build a program which reads in a wavefront (.obj) file, parses it into some graph-like structure, and applies Dijkstra's shortest path algorithm to it in order to find the shortest path (based on Euclidean distance) between any two faces. Finally, this path of faces is then outputted as a wavefront file.
### Roadmap
- Efficiently (hopefully) Parse the Wavefront File into a Graph-Like Structure Suitable for Pathfinding
- Implement an Efficient Shortest Path Solver Using Dijkstra's Shortest Path Algorithm
- Sacrifice a Few Triangles to the Corporate Mega-Archon
- Output Shortest Path as a Wavefront File