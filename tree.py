import tkinter as tk
from tkinter import messagebox

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTreeVisualizer:
    def __init__(self, root):
        self.root_node = None
        self.window = root
        self.window.title("Binary Tree Visualizer")

        self.canvas = tk.Canvas(self.window, width=900, height=400, bg="white")
        self.canvas.pack()

        self.entry = tk.Entry(self.window, font=("Arial", 14))
        self.entry.pack(pady=10)

        insert_button = tk.Button(self.window, text="Insert", command=self.insert_node, font=("Arial", 10), bg="lightblue")
        insert_button.pack(pady=5)

        inorder_button = tk.Button(self.window, text="Show Inorder Traversal", command=self.show_inorder, font=("Arial", 12), bg="lightgreen")
        inorder_button.pack(pady=5)

        preorder_button = tk.Button(self.window, text="Show Preorder Traversal", command=self.show_preorder, font=("Arial", 12), bg="lightyellow")
        preorder_button.pack(pady=5)

        postorder_button = tk.Button(self.window, text="Show Postorder Traversal", command=self.show_postorder, font=("Arial", 12), bg="lightpink")
        postorder_button.pack(pady=5)

        self.result_label = tk.Label(self.window, text="", font=("Arial", 14), wraplength=750, justify="left", bg="white", anchor="w")
        self.result_label.pack(pady=10, fill="x")

    def insert_node(self):
        try:
            value = int(self.entry.get())
            self.root_node = self._insert(self.root_node, value)
            self.entry.delete(0, tk.END)
            self.draw_tree()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")

    def _insert(self, root, value):
        if root is None:
            return TreeNode(value)
        if value < root.value:
            root.left = self._insert(root.left, value)
        else:
            root.right = self._insert(root.right, value)
        return root

    def show_inorder(self):
        result = []
        self._inorder(self.root_node, result)
        self.result_label.config(text="Inorder Traversal: " + ' '.join(map(str, result)))

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    def show_preorder(self):
        result = []
        self._preorder(self.root_node, result)
        self.result_label.config(text="Preorder Traversal: " + ' '.join(map(str, result)))

    def _preorder(self, node, result):
        if node:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def show_postorder(self):
        result = []
        self._postorder(self.root_node, result)
        self.result_label.config(text="Postorder Traversal: " + ' '.join(map(str, result)))

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)

    def draw_tree(self):
        self.canvas.delete("all")
        if self.root_node:
            self._draw_node(self.root_node, 400, 40, 200)

    def _draw_node(self, node, x, y, spacing):
        if node.left:
            self.canvas.create_line(x, y, x - spacing, y + 80, fill="black")
            self._draw_node(node.left, x - spacing, y + 80, spacing // 2)
        if node.right:
            self.canvas.create_line(x, y, x + spacing, y + 80, fill="black")
            self._draw_node(node.right, x + spacing, y + 80, spacing // 2)

        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="skyblue", outline="black")
        self.canvas.create_text(x, y, text=str(node.value), font=("Arial", 12, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryTreeVisualizer(root)
    root.mainloop()
