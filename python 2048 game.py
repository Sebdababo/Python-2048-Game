import random
import tkinter as tk
from tkinter import messagebox

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048")
        self.master.geometry("400x500")
        self.master.resizable(False, False)

        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.high_score = 0

        self.colors = {
            0: "#CDC1B4",
            2: "#EEE4DA",
            4: "#EDE0C8",
            8: "#F2B179",
            16: "#F59563",
            32: "#F67C5F",
            64: "#F65E3B",
            128: "#EDCF72",
            256: "#EDCC61",
            512: "#EDC850",
            1024: "#EDC53F",
            2048: "#EDC22E"
        }

        self.create_widgets()
        self.spawn_number()
        self.spawn_number()
        self.update_gui()

        self.master.bind("<Key>", self.key_press)

    def create_widgets(self):
        self.score_frame = tk.Frame(self.master)
        self.score_frame.pack(fill="x", padx=10, pady=10)

        self.score_label = tk.Label(self.score_frame, text="Score: 0", font=("Arial", 16))
        self.score_label.pack(side="left")

        self.high_score_label = tk.Label(self.score_frame, text="High Score: 0", font=("Arial", 16))
        self.high_score_label.pack(side="right")

        self.game_frame = tk.Frame(self.master, bg="#BBADA0")
        self.game_frame.pack(padx=10, pady=10)

        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(self.game_frame, width=90, height=90, bg="#CDC1B4")
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(cell_frame, text="", font=("Arial", 24, "bold"), bg="#CDC1B4")
                cell_number.place(relx=0.5, rely=0.5, anchor="center")
                row.append(cell_number)
            self.cells.append(row)

    def spawn_number(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def update_gui(self):
        for i in range(4):
            for j in range(4):
                num = self.board[i][j]
                self.cells[i][j].config(text=str(num) if num != 0 else "", bg=self.colors[num])
        self.score_label.config(text=f"Score: {self.score}")
        self.high_score_label.config(text=f"High Score: {self.high_score}")

    def move(self, direction):
        original_board = [row[:] for row in self.board]
        if direction in ['left', 'right']:
            for i in range(4):
                line = self.board[i]
                if direction == 'right':
                    line = line[::-1]
                merged_line = self.merge(line)
                if direction == 'right':
                    merged_line = merged_line[::-1]
                self.board[i] = merged_line
        elif direction in ['up', 'down']:
            for j in range(4):
                line = [self.board[i][j] for i in range(4)]
                if direction == 'down':
                    line = line[::-1]
                merged_line = self.merge(line)
                if direction == 'down':
                    merged_line = merged_line[::-1]
                for i in range(4):
                    self.board[i][j] = merged_line[i]
        return original_board != self.board

    def merge(self, line):
        new_line = [0] * 4
        idx = 0
        for i in range(4):
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
                    messagebox.showinfo("Congratulations", "You've reached 2048! You can continue playing.")

    def is_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return False
                if i < 3 and self.board[i][j] == self.board[i+1][j]:
                    return False
                if j < 3 and self.board[i][j] == self.board[i][j+1]:
                    return False
        return True

    def has_won(self):
        return any(2048 in row for row in self.board)

    def reset_game(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.spawn_number()
        self.spawn_number()
        self.update_gui()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()