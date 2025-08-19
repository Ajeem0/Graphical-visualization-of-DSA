import tkinter as tk
import subprocess
import sys
import os

# function to run another file
def run_file(filename):
    python = sys.executable
    subprocess.Popen([python, filename])

class DSAPlaygroundApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DSA Playground App")
        self.root.geometry("500x500")
        self.root.configure(bg="#f0f0f0")

        title = tk.Label(root, text="DSA Playground", font=("Arial", 22, "bold"), bg="#f0f0f0")
        title.pack(pady=20)

        # Buttons for each module
        tk.Button(root, text="Sorting Visualizer", width=30, height=2,
                  command=lambda: run_file("sort.py")).pack(pady=10)
        
        tk.Button(root, text="Tree Visualizer", width=30, height=2,
                  command=lambda: run_file("tree.py")).pack(pady=10)
        
        tk.Button(root, text="Traversal Visualizer", width=30, height=2,
                  command=lambda: run_file("traversal.py")).pack(pady=10)
        
        tk.Button(root, text="Heap Operations", width=30, height=2,
                  command=lambda: run_file("heap.py")).pack(pady=10)
        
        tk.Button(root, text="Sudoku Solver", width=30, height=2,
                  command=lambda: run_file("soduko_solver.py")).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = DSAPlaygroundApp(root)
    root.mainloop()

