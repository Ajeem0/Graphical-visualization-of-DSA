import tkinter as tk
from tkinter import messagebox
import time

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class BinaryTreeVisualizer:
    def __init__(self, root):
        self.root_node = None
        self.window = root
        self.window.title("Binary Tree Visualizer")

        self.canvas_frame = tk.Frame(self.window)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self.window, font=("Arial", 14))
        self.entry.pack(pady=10)

        insert_button = tk.Button(self.window, text="Insert", command=self.insert_node, font=("Arial", 12), bg="lightblue")
        insert_button.pack(pady=5)

        delete_button = tk.Button(self.window, text="Delete", command=self.delete_node, font=("Arial", 12), bg="tomato")
        delete_button.pack(pady=5)

        inorder_button = tk.Button(self.window, text="Show Inorder Traversal", command=self.show_inorder, font=("Arial", 12), bg="lightgreen")
        inorder_button.pack(pady=5)

        preorder_button = tk.Button(self.window, text="Show Preorder Traversal", command=self.show_preorder, font=("Arial", 12), bg="lightyellow")
        preorder_button.pack(pady=5)

        postorder_button = tk.Button(self.window, text="Show Postorder Traversal", command=self.show_postorder, font=("Arial", 12), bg="lightpink")
        postorder_button.pack(pady=5)

        dfs_button = tk.Button(self.window, text="Animate DFS Traversal", command=self.animate_dfs, font=("Arial", 12), bg="orange")
        dfs_button.pack(pady=5)

        avl_button = tk.Button(self.window, text="Convert to AVL Tree (Animated)", command=self.convert_to_avl_animated, font=("Arial", 12), bg="lightgray")
        avl_button.pack(pady=5)

        self.result_label = tk.Label(self.window, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.node_positions = {}  # Stores node coordinates for animation

        self.window.bind("<Configure>", lambda event: self.draw_tree())

    def insert_node(self):
        try:
            value = int(self.entry.get())
            self.root_node = self._insert(self.root_node, value)
            self.entry.delete(0, tk.END)
            self.draw_tree()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")

    def delete_node(self):
        try:
            value = int(self.entry.get())
            self.root_node = self._delete(self.root_node, value)
            self.entry.delete(0, tk.END)
            self.draw_tree()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")

    def _insert(self, root, value):
        # Time Complexity: O(log n) average, O(n) worst-case
        # Space Complexity: O(log n) due to recursion stack
        if root is None:
            return TreeNode(value)
        if value < root.value:
            root.left = self._insert(root.left, value)
        else:
            root.right = self._insert(root.right, value)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and value < root.left.value:
            return self.right_rotate(root)
        if balance < -1 and value > root.right.value:
            return self.left_rotate(root)
        if balance > 1 and value > root.left.value:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and value < root.right.value:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def _delete(self, root, value):
        # Time Complexity: O(log n) average, O(n) worst-case
        # Space Complexity: O(log n)
        if not root:
            return root

        if value < root.value:
            root.left = self._delete(root.left, value)
        elif value > root.value:
            root.right = self._delete(root.right, value)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            temp = self.get_min_value_node(root.right)
            root.value = temp.value
            root.right = self._delete(root.right, temp.value)

        if not root:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def get_min_value_node(self, root):
        current = root
        while current.left:
            current = current.left
        return current

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def convert_to_avl_animated(self):
        # Time Complexity: O(n log n)
        # Space Complexity: O(n)
        values = []
        self._inorder(self.root_node, values)
        self.root_node = None

        for val in values:
            self.root_node = self._insert(self.root_node, val)
            self.draw_tree()
            time.sleep(0.5)
            self.window.update()

        messagebox.showinfo("AVL Conversion", "Tree converted to AVL with animation!")
        self.draw_tree()

    def show_inorder(self):
        result = []
        self._inorder(self.root_node, result)
        self.result_label.config(text="Inorder Traversal: " + ' '.join(map(str, result)))

    def _inorder(self, node, result):
        # Time Complexity: O(n), Space Complexity: O(n)
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    def show_preorder(self):
        result = []
        self._preorder(self.root_node, result)
        self.result_label.config(text="Preorder Traversal: " + ' '.join(map(str, result)))

    def _preorder(self, node, result):
        # Time Complexity: O(n), Space Complexity: O(n)
        if node:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def show_postorder(self):
        result = []
        self._postorder(self.root_node, result)
        self.result_label.config(text="Postorder Traversal: " + ' '.join(map(str, result)))

    def _postorder(self, node, result):
        # Time Complexity: O(n), Space Complexity: O(n)
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)

    def draw_tree(self):
        self.canvas.delete("all")
        self.node_positions.clear()
        if self.root_node:
            width = self.canvas.winfo_width()
            self._draw_node(self.root_node, width // 2, 40, width // 4)

    def _draw_node(self, node, x, y, spacing):
        if node.left:
            self.canvas.create_line(x, y, x - spacing, y + 80, fill="black")
            self._draw_node(node.left, x - spacing, y + 80, spacing // 2)
        if node.right:
            self.canvas.create_line(x, y, x + spacing, y + 80, fill="black")
            self._draw_node(node.right, x + spacing, y + 80, spacing // 2)

        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="skyblue", outline="black")
        self.canvas.create_text(x, y, text=str(node.value), font=("Arial", 12, "bold"))
        self.node_positions[node] = (x, y)

    def animate_dfs(self):
        self._animate_dfs(self.root_node)

    def _animate_dfs(self, node):
        # Time Complexity: O(n), Space Complexity: O(n)
        if node:
            x, y = self.node_positions.get(node, (0, 0))
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="orange", outline="black")
            self.canvas.create_text(x, y, text=str(node.value), font=("Arial", 12, "bold"))
            self.window.update()
            time.sleep(0.5)
            self._animate_dfs(node.left)
            self._animate_dfs(node.right)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")
    app = BinaryTreeVisualizer(root)
    root.mainloop()