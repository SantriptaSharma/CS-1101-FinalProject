from os import path
from Parser import Parse

def main():
    file_path = input("Enter Path to .obj File: ")
    
    if(not path.exists(file_path)):
        print(f"File {path.abspath(file_path)} not found.")
        exit(1)
    with open(file_path, "r") as f:
        results = Parse(f)
        results.display()

if __name__ == "__main__":
    main()