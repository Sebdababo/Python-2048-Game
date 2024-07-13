import random
import tkinter as tk
from tkinter import messagebox

class Game2048:
    def __init__(self, master, size=4, win_value=2048):
        self.master = master
        self.master.title("2048")
        self.size = size
        self.win_value = win_value
        self.cell_size = 100
        self.padding = 10
        self.window_width = self.cell_size * self.size + self.padding * (self.size + 1)
        self.window_height = self.window_width + 100

        self.master.geometry(f"{self.window_width}x{self.window_height}")
        self.master.resizable(True, True)

        self.board = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.high_score = 0

        self.colors = {
            0: ("#CDC1B4", "#776E65"),
            2: ("#EEE4DA", "#776E65"),
            4: ("#EDE0C8", "#776E65"),
            8: ("#F2B179", "#F9F6F2"),
            16: ("#F59563", "#F9F6F2"),
            32: ("#F67C5F", "#F9F6F2"),
            64: ("#F65E3B", "#F9F6F2"),
            128: ("#EDCF72", "#F9F6F2"),
            256: ("#EDCC61", "#F9F6F2"),
            512: ("#EDC850", "#F9F6F2"),
            1024: ("#EDC53F", "#F9F6F2"),
            2048: ("#EDC22E", "#F9F6F2")
        }

        self.create_widgets()
        self.spawn_number(2)
        self.update_gui()

        self.master.bind("<Key>", self.key_press)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.master.focus_force()

    def create_widgets(self):
        self.score_frame = tk.Frame(self.master)
        self.score_frame.pack(fill="x", padx=10, pady=10)

        self.score_label = tk.Label(self.score_frame, text="Score: 0", font=("Arial", 16))
        self.score_label.pack(side="left")

        self.high_score_label = tk.Label(self.score_frame, text="High Score: 0", font=("Arial", 16))
        self.high_score_label.pack(side="right")

        self.game_frame = tk.Frame(self.master, bg="#BBADA0")
        self.game_frame.pack(padx=10, pady=10, expand=True, fill="both")

        self.cells = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                cell_frame = tk.Frame(self.game_frame, width=self.cell_size, height=self.cell_size)
                cell_frame.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                cell_label = tk.Label(cell_frame, text="", font=("Arial", 36, "bold"), justify="center")
                cell_label.pack(expand=True, fill="both")
                row.append(cell_label)
            self.cells.append(row)

        for i in range(self.size):
            self.game_frame.grid_rowconfigure(i, weight=1)
            self.game_frame.grid_columnconfigure(i, weight=1)

    def spawn_number(self, count=1):
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == 0]
        for _ in range(min(count, len(empty_cells))):
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4
            empty_cells.remove((i, j))

    def update_gui(self):
        for i in range(self.size):
            for j in range(self.size):
                num = self.board[i][j]
                cell = self.cells[i][j]
                bg_color, fg_color = self.colors.get(num, ("#ff0000", "#ffffff"))
                cell.config(
                    text=str(num) if num != 0 else "",
                    bg=bg_color,
                    fg=fg_color,
                    font=("Arial", 36 if num < 1000 else 28, "bold")
                )
        self.score_label.config(text=f"Score: {self.score}")
        self.high_score_label.config(text=f"High Score: {self.high_score}")

    def move(self, direction):
        original_board = [row[:] for row in self.board]
        if direction in ['left', 'right']:
            for i in range(self.size):
                line = self.board[i]
                if direction == 'right':
                    line = line[::-1]
                merged_line = self.merge(line)
                if direction == 'right':
                    merged_line = merged_line[::-1]
                self.board[i] = merged_line
        elif direction in ['up', 'down']:
            for j in range(self.size):
                line = [self.board[i][j] for i in range(self.size)]
                if direction == 'down':
                    line = line[::-1]
                merged_line = self.merge(line)
                if direction == 'down':
                    merged_line = merged_line[::-1]
                for i in range(self.size):
                    self.board[i][j] = merged_line[i]
        return original_board != self.board

    def merge(self, line):
        new_line = [0] * self.size
        idx = 0
        for i in range(self.size):
            if line[i] != 0:
                if idx > 0 and new_line[idx-1] == line[i]:
                    new_line[idx-1] *= 2
                    self.score += new_line[idx-1]
                    if self.score > self.high_score:
                        self.high_score = self.score
                else:
                    new_line[idx] = line[i]
                    idx += 1
        return new_line

    def key_press(self, event):
        key = event.keysym.lower()
        if key in ['left', 'right', 'up', 'down']:
            changed = self.move(key)
            if changed:
                self.spawn_number()
                self.update_gui()
                if self.is_game_over():
                    messagebox.showinfo("Game Over", f"Game Over! Your score: {self.score}")
                    self.reset_game()
                elif self.has_won():
                    if messagebox.askyesno("Congratulations", f"You've reached {self.win_value}! Do you want to continue playing?"):
                        self.win_value *= 2
                    else:
                        self.reset_game()

    def is_game_over(self):
        if any(0 in row for row in self.board):
            return False
        for i in range(self.size):
            for j in range(self.size):
                if j < self.size - 1 and self.board[i][j] == self.board[i][j+1]:
                    return False
                if i < self.size - 1 and self.board[i][j] == self.board[i+1][j]:
                    return False
        return True

    def has_won(self):
        return any(self.win_value in row for row in self.board)

    def reset_game(self):
        self.board = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.win_value = 2048
        self.spawn_number(2)
        self.update_gui()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit the game?"):
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()