import tkinter as tk
from tkinter import messagebox
import heapq
import time

class HeapVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Heap Visualizer")
        self.data = []  # For max or min heap input
        self.is_min_heap = True

        self.canvas = tk.Canvas(root, width=800, height=500, bg="white")
        self.canvas.pack()

        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack(pady=5)

        self.insert_button = tk.Button(root, text="Insert", command=self.insert_value)
        self.insert_button.pack(pady=2)

        self.toggle_button = tk.Button(root, text="Switch to Max Heap", command=self.toggle_heap_type)
        self.toggle_button.pack(pady=2)

        self.sort_button = tk.Button(root, text="Visualize Heap Sort", command=self.visualize_heap_sort)
        self.sort_button.pack(pady=2)

        self.label = tk.Label(root, text="Min Heap", font=("Arial", 14))
        self.label.pack(pady=10)

    def toggle_heap_type(self):
        self.is_min_heap = not self.is_min_heap
        self.label.config(text="Min Heap" if self.is_min_heap else "Max Heap")
        self.toggle_button.config(text="Switch to Max Heap" if self.is_min_heap else "Switch to Min Heap")
        self.data.clear()
        self.canvas.delete("all")

    def insert_value(self):
        try:
            val = int(self.entry.get())
            self.entry.delete(0, tk.END)
            if self.is_min_heap:
                heapq.heappush(self.data, val)
            else:
                heapq.heappush(self.data, -val)
            self.draw_heap()
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a valid integer")

    def draw_heap(self):
        self.canvas.delete("all")
        heap = self.data[:]
        if not heap:
            return

        positions = {}

        def draw_node(index, x, y, dx):
            if index >= len(heap):
                return
            value = heap[index]
            value = value if self.is_min_heap else -value
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="lightblue")
            self.canvas.create_text(x, y, text=str(value), font=("Arial", 12))
            positions[index] = (x, y)

            left = 2 * index + 1
            right = 2 * index + 2

            if left < len(heap):
                self.canvas.create_line(x, y, x - dx, y + 80)
                draw_node(left, x - dx, y + 80, dx // 2)
            if right < len(heap):
                self.canvas.create_line(x, y, x + dx, y + 80)
                draw_node(right, x + dx, y + 80, dx // 2)

        draw_node(0, 400, 40, 120)

    def visualize_heap_sort(self):
        if not self.data:
            return

        heap = self.data[:]
        if not self.is_min_heap:
            heap = [-x for x in heap]
            heapq.heapify(heap)

        sorted_list = []

        self.canvas.delete("all")
        x = 60
        for i in range(len(heap)):
            val = heapq.heappop(heap)
            sorted_list.append(val)
            self.canvas.create_rectangle(x, 300, x + 40, 340, fill="orange")
            self.canvas.create_text(x + 20, 320, text=str(val if self.is_min_heap else -val))
            self.root.update()
            time.sleep(0.5)
            x += 50

        final = [val if self.is_min_heap else -val for val in sorted_list]
        messagebox.showinfo("Heap Sort Done", f"Sorted: {final}")

if __name__ == "__main__":
    window = tk.Tk()
    app = HeapVisualizer(window)
    window.mainloop()
