import tkinter as tk
from tkinter import messagebox
import time
import sys
import tracemalloc

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithms Visualizer")

        self.canvas = tk.Canvas(root, width=900, height=400, bg="white")
        self.canvas.pack()

        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack(pady=5)

        self.insert_button = tk.Button(root, text="Insert (comma-separated)", command=self.insert_values)
        self.insert_button.pack(pady=2)

        self.speed_scale = tk.Scale(root, from_=1, to=500, orient=tk.HORIZONTAL, label="Adjust Speed (ms)")
        self.speed_scale.set(100)
        self.speed_scale.pack(pady=5)

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()

        algorithms = [
            ("Bubble Sort", self.visualize_bubble_sort),
            ("Selection Sort", self.visualize_selection_sort),
            ("Insertion Sort", self.visualize_insertion_sort),
            ("Merge Sort", self.visualize_merge_sort),
            ("Quick Sort", self.visualize_quick_sort),
            ("Heap Sort", self.visualize_heap_sort),
            ("Bucket Sort", self.visualize_bucket_sort),
        ]

        for name, func in algorithms:
            tk.Button(self.buttons_frame, text=name, command=lambda f=func, n=name: self.track_complexity(f, n)).pack(side=tk.LEFT, padx=5, pady=5)

        self.values = []

    def insert_values(self):
        try:
            self.values = list(map(int, self.entry.get().split(',')))
            self.entry.delete(0, tk.END)
            self.draw_bars(self.values, color='skyblue')
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter comma-separated integers")

    def draw_bars(self, values, color='skyblue', highlight_indices=[]):
        self.canvas.delete("all")
        width = 20
        spacing = 10
        for i, val in enumerate(values):
            x0 = i * (width + spacing) + 50
            y0 = 350 - val * 3
            x1 = x0 + width
            y1 = 350
            bar_color = color
            if i in highlight_indices:
                bar_color = 'red'
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=bar_color)
            self.canvas.create_text(x0 + width//2, y0 - 10, text=str(val), font=("Arial", 10))
        self.root.update()

    def sleep(self):
        time.sleep(self.speed_scale.get() / 1000.0)

    def track_complexity(self, sort_func, name):
        arr_copy = self.values[:]
        tracemalloc.start()
        start_time = time.perf_counter()
        sort_func()
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        duration = (end_time - start_time) * 1000
        messagebox.showinfo(f"{name} Complexity", f"Time Taken: {duration:.2f} ms\nPeak Memory Used: {peak / 1024:.2f} KB")

    def visualize_bubble_sort(self):
        arr = self.values[:]
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                self.draw_bars(arr, highlight_indices=[j, j+1])
                self.sleep()
        self.draw_bars(arr, color='orange')

    def visualize_selection_sort(self):
        arr = self.values[:]
        for i in range(len(arr)):
            min_idx = i
            for j in range(i+1, len(arr)):
                if arr[j] < arr[min_idx]:
                    min_idx = j
                self.draw_bars(arr, highlight_indices=[min_idx, j])
                self.sleep()
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        self.draw_bars(arr, color='orange')

    def visualize_insertion_sort(self):
        arr = self.values[:]
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >=0 and key < arr[j]:
                arr[j+1] = arr[j]
                j -= 1
                self.draw_bars(arr, highlight_indices=[j+1, j+2])
                self.sleep()
            arr[j+1] = key
        self.draw_bars(arr, color='orange')

    def visualize_merge_sort(self):
        def merge_sort(arr, left, right):
            if left < right:
                mid = (left + right) // 2
                merge_sort(arr, left, mid)
                merge_sort(arr, mid+1, right)
                merge(arr, left, mid, right)

        def merge(arr, left, mid, right):
            L = arr[left:mid+1]
            R = arr[mid+1:right+1]
            i = j = 0
            k = left
            while i < len(L) and j < len(R):
                if L[i] <= R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                self.draw_bars(arr, highlight_indices=[k])
                self.sleep()
                k += 1

            while i < len(L):
                arr[k] = L[i]
                i += 1
                self.draw_bars(arr, highlight_indices=[k])
                self.sleep()
                k += 1
            while j < len(R):
                arr[k] = R[j]
                j += 1
                self.draw_bars(arr, highlight_indices=[k])
                self.sleep()
                k += 1

        arr = self.values[:]
        merge_sort(arr, 0, len(arr) - 1)
        self.draw_bars(arr, color='orange')

    def visualize_quick_sort(self):
        def quick_sort(arr, low, high):
            if low < high:
                pi = partition(arr, low, high)
                quick_sort(arr, low, pi - 1)
                quick_sort(arr, pi + 1, high)

        def partition(arr, low, high):
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    self.draw_bars(arr, highlight_indices=[i, j])
                    self.sleep()
            arr[i+1], arr[high] = arr[high], arr[i+1]
            self.draw_bars(arr, highlight_indices=[i+1, high])
            self.sleep()
            return i + 1

        arr = self.values[:]
        quick_sort(arr, 0, len(arr) - 1)
        self.draw_bars(arr, color='orange')

    def visualize_heap_sort(self):
        def heapify(arr, n, i):
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2
            if l < n and arr[l] > arr[largest]:
                largest = l
            if r < n and arr[r] > arr[largest]:
                largest = r
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                self.draw_bars(arr, highlight_indices=[i, largest])
                self.sleep()
                heapify(arr, n, largest)

        arr = self.values[:]
        n = len(arr)
        for i in range(n//2 - 1, -1, -1):
            heapify(arr, n, i)
        for i in range(n-1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            self.draw_bars(arr, highlight_indices=[0, i])
            self.sleep()
            heapify(arr, i, 0)
        self.draw_bars(arr, color='orange')

    def visualize_bucket_sort(self):
        if not self.values:
            return

        arr = self.values[:]
        max_val = max(arr)
        bucket_count = 10
        buckets = [[] for _ in range(bucket_count)]

        for val in arr:
            index = min(bucket_count - 1, val * bucket_count // (max_val + 1))
            buckets[index].append(val)
            self.draw_bars(arr, highlight_indices=[arr.index(val)])
            self.sleep()

        sorted_array = []
        for bucket in buckets:
            sorted_bucket = sorted(bucket)
            sorted_array.extend(sorted_bucket)

        self.draw_bars(sorted_array, color='orange')
        messagebox.showinfo("Bucket Sort", f"Sorted Array: {sorted_array}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
