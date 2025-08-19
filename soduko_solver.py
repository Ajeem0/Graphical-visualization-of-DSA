import tkinter as tk
from tkinter import messagebox

class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver - Backtracking")

        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.board = [[0 for _ in range(9)] for _ in range(9)]

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        for i in range(9):
            for j in range(9):
                e = tk.Entry(self.frame, width=2, font=('Arial', 18), justify='center')
                e.grid(row=i, column=j, padx=1, pady=1, ipadx=5, ipady=5)
                self.entries[i][j] = e

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.solve_button = tk.Button(self.button_frame, text="Solve", command=self.solve)
        self.solve_button.pack(side='left', padx=10)

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_board)
        self.clear_button.pack(side='left', padx=10)

    def read_board(self):
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                self.board[i][j] = int(val) if val.isdigit() else 0

    def display_board(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(self.board[i][j]))

    def is_valid(self, row, col, num):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False

        return True

    def solve_sudoku(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num
                            if self.solve_sudoku():
                                return True
                            self.board[row][col] = 0
                    return False
        return True

    def solve(self):
        self.read_board()
        if self.solve_sudoku():
            self.display_board()
        else:
            messagebox.showerror("Error", "No solution exists for the given Sudoku")

    def clear_board(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
        self.board = [[0 for _ in range(9)] for _ in range(9)]

if __name__ == '__main__':
    root = tk.Tk()
    app = SudokuSolver(root)
    root.mainloop()
