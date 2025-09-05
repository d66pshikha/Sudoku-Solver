import tkinter as tk
from tkinter import messagebox
import threading
import time
class SudokuGUI:


    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver (Tkinter GUI)")

        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()
        self.create_solve_button()
        #hashing
        self.rows = [[False]*10 for _ in range(9)]
        self.cols = [[False]*10 for _ in range(9)]
        self.boxes = [[False]*10 for _ in range(9)]

    def create_grid(self):
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.root, width=3, font=('Arial', 18), justify='center')
                entry.grid(row=i, column=j, padx=1, pady=1)
                self.entries[i][j] = entry
                if (i // 3 + j // 3) % 2 == 0:
                    entry.configure(bg="#f0f0f0")

    def create_solve_button(self):
        solve_button = tk.Button(
            self.root,
            text="Solve",
            command=self.solve_puzzle,
            font=('Arial', 14),
            bg="#4CAF50",
            fg="white"
        )
        solve_button.grid(row=9, column=0, columnspan=9, sticky='we', padx=1, pady=5)

    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                row.append(int(val) if val.isdigit() and 1 <= int(val) <= 9 else 0)
            board.append(row)
        return board

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if board[i][j] != 0:
                    self.entries[i][j].insert(0, str(board[i][j]))

    # is_board_valid now also initializes hash sets
    def is_board_valid(self, board):
        """Check if board is valid and initialize hash sets."""
        # Clear all hash sets first
        for i in range(9):
            for num in range(10):
                self.rows[i][num] = False
                self.cols[i][num] = False
                self.boxes[i][num] = False

        for i in range(9):
            for j in range(9):
                num = board[i][j]
                if num != 0:
                    box_index = (i // 3) * 3 + (j // 3)
                    if self.rows[i][num] or self.cols[j][num] or self.boxes[box_index][num]:
                        return False
                    #  ADDED: update hash sets
                    self.rows[i][num] = True
                    self.cols[j][num] = True
                    self.boxes[box_index][num] = True
        return True

    #solve_puzzle runs solver in a thread
    def solve_puzzle(self):
        board = self.get_board()
        if not self.is_board_valid(board):
            messagebox.showerror("Sudoku Solver", "Invalid puzzle! Check input.")
            return

        def run_solver():
            start = time.time()#  ADDED: start timer
            if self.solve(board):
                end = time.time()  # - ADDED: end timer
                duration = end - start
                self.root.after(0, lambda: (
                    self.set_board(board),
                    messagebox.showinfo("Sudoku Solver", f"Puzzle Solved!\n\nTime Taken: {duration:.4f} seconds")
                ))
            else:
                self.root.after(0, lambda: messagebox.showerror("Sudoku Solver", "❌ Cannot solve this puzzle."))

        threading.Thread(target=run_solver, daemon=True).start()

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    # is_valid uses hash sets
    def is_valid(self, board, num, pos):
        row, col = pos
        box_index = (row // 3) * 3 + (col // 3)
        return not (self.rows[row][num] or self.cols[col][num] or self.boxes[box_index][num])

    # ADDED: helper to place number and update hash sets
    def place_number(self, board, num, pos):
        row, col = pos
        board[row][col] = num
        box_index = (row // 3) * 3 + (col // 3)
        self.rows[row][num] = True
        self.cols[col][num] = True
        self.boxes[box_index][num] = True

    #  ADDED: helper to remove number (backtracking)
    def remove_number(self, board, num, pos):
        row, col = pos
        board[row][col] = 0
        box_index = (row // 3) * 3 + (col // 3)
        self.rows[row][num] = False
        self.cols[col][num] = False
        self.boxes[box_index][num] = False

    # solve uses place_number/remove_number
    def solve(self, board):
        find = self.find_empty(board)
        if not find:
            return True
        row, col = find

        for num in range(1, 10):
            if self.is_valid(board, num, (row, col)):
                self.place_number(board, num, (row, col))  # use hash
                if self.solve(board):
                    return True
                self.remove_number(board, num, (row, col))  # backtrack with hash
        return False


if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
