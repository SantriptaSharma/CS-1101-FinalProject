from os import path
from Parser import Parse
from Graph import ParseIntoGraph

def main():
    file_path = input("Enter Path to .obj File: ")
    
    if(not path.exists(file_path)):
        print(f"File {path.abspath(file_path)} not found.")
        exit(1)

    results = None
    with open(file_path, "r") as f:
        results = Parse(f)
    
    results.display()
    graph = ParseIntoGraph(results)

    print("-"*30)
    print("GRAPH DATA DUMP")
    print(graph.data)
    print("-"*30)

if __name__ == "__main__":
    main()