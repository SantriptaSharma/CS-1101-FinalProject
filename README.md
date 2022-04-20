# PolyTraverse
### Goal
To build a program which reads in a wavefront (.obj) file, parses it into some graph-like structure, and applies Dijkstra's shortest path algorithm to it in order to find the shortest path (based on Euclidean distance) between any two faces. Finally, this path of faces is then outputted as a wavefront file.
### Roadmap
<html>
<style>
    .item
    {
        display: block;
        padding: 14px 10px;
        margin: 10px auto 50px auto;
        border: solid 2px;
        border-radius: 8px;
        position: relative;
    }
</style>
<style>
    .item:not(.last)::after
    {
        box-sizing: border-box;
        position: absolute;
        left: 49%;
        top: calc(50% + 31px);
        transform: translate(-50%, 0);
        content: "";
        border: dotted 2px;
        border-radius: 3px;
        width: 4px;
        height: 40px;
    }
</style>
<!--Why does each style need to be in a new tag for it to be recognised? weird.-->
<style>
    .done
    {
        text-decoration: line-through;
        color: #8cc63f;
    }
</style>
<div class = "box">
    <span class = "item done"> Spend an Unnecessary Amount of Time Building an Overly-Complex Readme File</span>
    <span class = "item"> Efficiently (hopefully) Parse the Wavefront File into a Graph-Like Structure Suitable for Pathfinding</span>
    <span class = "item"> Implement an Efficient Shortest Path Solver Using Dijkstra's Shortest Path Algorithm</span>
    <span class = "item"> Sacrifice a Few Triangles to the Corporate Mega-Archon</span>
    <span class = "item last"> Output the Shortest Path (through connected faces) Between Any Two Given Faces as a Wavefront File</span>
</div>
</html>