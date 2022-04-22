from os import path, scandir
from Parser import Parse
from Graph import ParseIntoGraph

def main():
    use_examples = input("Use Examples? (y)/n: ")
    if(use_examples.upper() == "N"):
        use_examples = False
    else:
        use_examples = True
    
    final_file_path = ""

    if use_examples:
        examples_dir = "examples"

        while(not path.isdir(examples_dir)):
            choice = input(f"Examples directory not found at {path.abspath(examples_dir)}, would you like to specify an examples directory? y/(n): ")
            if(choice.upper() != "Y"):
                use_examples = False
                break

            examples_dir = input("Enter path to examples directory: ")
        
        options = []

        for thing in scandir(examples_dir):
            if(thing.is_file and thing.name.endswith(".obj")):
                options.append(thing.name)

        print()
        for (i, obj) in enumerate(options):
            print(f"{i+1}: {obj}")
        
        choice = 0

        while choice not in range(1, len(options)+1):
            choice = input(f"Choose (1 to {len(options)}): ")

            if(not choice.isnumeric):
                print("Not a valid choice")
                continue
            
            choice = int(choice)

            if(choice not in range(1, len(options)+1)):
                print("Not a valid choice")
                continue
        
        final_file_path = path.join(examples_dir, options[choice-1])

    if not use_examples:
        file_path = input("Enter Path to .obj File: ")
        
        if(not path.exists(file_path)):
            print(f"File {path.abspath(file_path)} not found.")
            exit(1)
        
        final_file_path = file_path
    
    results = None
    with open(final_file_path, "r") as f:
        results = Parse(f)
    
    graph = ParseIntoGraph(results, 1)

    print("-"*30)
    print("GRAPH DATA DUMP")
    print(graph.data)
    print("-"*30)

if __name__ == "__main__":
    main()