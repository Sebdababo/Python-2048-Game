import random
import os
import msvcrt

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    clear_console()
    for row in board:
        print('+' + '-----+' * 4)
        print('|' + '|'.join(f'{num:^5}' for num in row) + '|')
    print('+' + '-----+' * 4)

def spawn_number(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

def move(board, direction):
    def merge(row):
        new_row = [0] * 4
        idx = 0
        for i in range(4):
            if row[i] != 0:
                if idx > 0 and new_row[idx-1] == row[i]:
                    new_row[idx-1] *= 2
                else:
                    new_row[idx] = row[i]
                    idx += 1
        return new_row

    changed = False
    if direction in ['left', 'right']:
        for i in range(4):
            row = board[i]
            if direction == 'right':
                row = row[::-1]
            new_row = merge(row)
            if direction == 'right':
                new_row = new_row[::-1]
            if row != new_row:
                changed = True
            board[i] = new_row
    elif direction in ['up', 'down']:
        for j in range(4):
            col = [board[i][j] for i in range(4)]
            if direction == 'down':
                col = col[::-1]
            new_col = merge(col)
            if direction == 'down':
                new_col = new_col[::-1]
            if col != new_col:
                changed = True
            for i in range(4):
                board[i][j] = new_col[i]
    return changed

def is_game_over(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
            if i < 3 and board[i][j] == board[i+1][j]:
                return False
            if j < 3 and board[i][j] == board[i][j+1]:
                return False
    return True

def main():
    board = [[0] * 4 for _ in range(4)]
    spawn_number(board)
    spawn_number(board)

    while True:
        print_board(board)
        
        key = msvcrt.getch()
        if key == b'\xe0':
            key = msvcrt.getch()
            if key == b'H':
                changed = move(board, 'up')
            elif key == b'P':
                changed = move(board, 'down')
            elif key == b'K':
                changed = move(board, 'left')
            elif key == b'M':
                changed = move(board, 'right')
            else:
                continue

            if changed:
                spawn_number(board)

            if is_game_over(board):
                print_board(board)
                print("Game Over!")
                break

if __name__ == "__main__":
    main()