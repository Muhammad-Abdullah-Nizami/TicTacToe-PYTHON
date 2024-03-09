import tkinter as tk
from tkinter import messagebox


PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = " "
BOARD_SIZE = 3

def create_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def is_winner(board, player):
    for row in range(BOARD_SIZE):
        if all(board[row][col] == player for col in range(BOARD_SIZE)):
            return True

    for col in range(BOARD_SIZE):
        if all(board[row][col] == player for row in range(BOARD_SIZE)):
            return True

    if all(board[i][i] == player for i in range(BOARD_SIZE)):
        return True

    if all(board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)):
        return True

    return False

def is_draw(board):
    return all(board[row][col] != EMPTY for row in range(BOARD_SIZE) for col in range(BOARD_SIZE))

def is_game_over(board):
    return is_winner(board, PLAYER_X) or is_winner(board, PLAYER_O) or is_draw(board)

def get_empty_cells(board):
    return [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE) if board[row][col] == EMPTY]

def on_click(row, col):
    if board[row][col] == EMPTY and not is_game_over(board):
        player = PLAYER_X if x_turn.get() else PLAYER_O
        board[row][col] = player
        buttons[row][col].config(text=player, state=tk.DISABLED)

        if is_winner(board, PLAYER_X):
            messagebox.showinfo("Game Over", "Player X wins!")
            disable_buttons()
        elif is_winner(board, PLAYER_O):
            messagebox.showinfo("Game Over", "Player O wins!")
            disable_buttons()
        elif is_draw(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            disable_buttons()
        else:
            x_turn.set(not x_turn.get())
            if ai_mode.get() == 1 and not x_turn.get():
                ai_move_heuristic()
            elif ai_mode.get() == 2 and not x_turn.get():
                ai_move_minimax()

def on_reset():
    reset_game()

def ai_move_heuristic():
    if not is_game_over(board) and not x_turn.get() and ai_mode.get() == 1 and players_mode.get() == 1:
        for row, col in get_empty_cells(board):
            board[row][col] = PLAYER_O
            if is_winner(board, PLAYER_O):
                buttons[row][col].config(text=PLAYER_O, state=tk.DISABLED)
                messagebox.showinfo("Game Over", "Player O wins!")
                disable_buttons()
                return
            board[row][col] = EMPTY

        for row, col in get_empty_cells(board):
            board[row][col] = PLAYER_X
            if is_winner(board, PLAYER_X):
                board[row][col] = PLAYER_O
                buttons[row][col].config(text=PLAYER_O, state=tk.DISABLED)
                x_turn.set(True)
                return
            board[row][col] = EMPTY

        for row, col in get_empty_cells(board):
            board[row][col] = PLAYER_O
            buttons[row][col].config(text=PLAYER_O, state=tk.DISABLED)
            x_turn.set(True)
            break

def ai_move_minimax():
    if not is_game_over(board) and not x_turn.get() and ai_mode.get() == 2 and players_mode.get() == 1:
        best_score = -float("inf")
        best_move = None

        for row, col in get_empty_cells(board):
            board[row][col] = PLAYER_O
            score = minimax(board, 0, False)
            board[row][col] = EMPTY

            if score > best_score:
                best_score = score
                best_move = (row, col)

        if best_move:
            row, col = best_move
            board[row][col] = PLAYER_O
            buttons[row][col].config(text=PLAYER_O, state=tk.DISABLED)

            if is_winner(board, PLAYER_O):
                messagebox.showinfo("Game Over", "Player O wins!")
                disable_buttons()
            elif is_draw(board):
                messagebox.showinfo("Game Over", "It's a draw!")
                disable_buttons()
            else:
                x_turn.set(True)
	

def minimax(board, depth, is_maximizing):
    if is_winner(board, PLAYER_X):
        return -1
    if is_winner(board, PLAYER_O):
        return 1
    if is_draw(board):
        return 0
    if is_maximizing:
        best_score = -float("inf")
        for row, col in get_empty_cells(board):
            board[row][col] = PLAYER_O
            score = minimax(board, depth + 1, False)
            board[row][col] = EMPTY
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row, col in get_empty_cells(board):
            board[row][col] = PLAYER_X
            score = minimax(board, depth + 1, True)
            board[row][col] = EMPTY
            best_score = min(score, best_score)
        return best_score

def disable_buttons():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            buttons[row][col].config(state=tk.DISABLED)

def reset_game():
    global board
    board = create_board()
    x_turn.set(True)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            buttons[row][col].config(text=EMPTY, state=tk.NORMAL)

#
app = tk.Tk()
app.title("Tic-Tac-Toe")


board = create_board()


buttons = []
for row in range(BOARD_SIZE):
    row_buttons = []
    for col in range(BOARD_SIZE):
        button = tk.Button(app, text=EMPTY, width=10, height=4, command=lambda r=row, c=col: on_click(r, c))
        button.grid(row=row, column=col)
        row_buttons.append(button)
    buttons.append(row_buttons)


players_label = tk.Label(app, text="Select Number of Players:")
players_label.grid(row=BOARD_SIZE, column=0, columnspan=BOARD_SIZE)

players_mode = tk.IntVar()
players_mode.set(1)
one_player_radio = tk.Radiobutton(app, text="One Player", variable=players_mode, value=1, command=reset_game)
one_player_radio.grid(row=BOARD_SIZE + 1, column=0, columnspan=BOARD_SIZE // 2)


two_players_radio = tk.Radiobutton(app, text="Two Players", variable=players_mode, value=2, command=reset_game)
two_players_radio.grid(row=BOARD_SIZE + 1, column=BOARD_SIZE // 2, columnspan=BOARD_SIZE // 2)


algorithm_label = tk.Label(app, text="Select Algorithm:")
algorithm_label.grid(row=BOARD_SIZE + 2, column=0, columnspan=BOARD_SIZE)


ai_mode = tk.IntVar()
ai_mode.set(1)
heuristic_radio = tk.Radiobutton(app, text="Heuristic", variable=ai_mode, value=1, command=reset_game)
heuristic_radio.grid(row=BOARD_SIZE + 3, column=0, columnspan=BOARD_SIZE // 2)


minimax_radio = tk.Radiobutton(app, text="Minimax", variable=ai_mode, value=2, command=reset_game)
minimax_radio.grid(row=BOARD_SIZE + 3, column=BOARD_SIZE // 2, columnspan=BOARD_SIZE // 2)


reset_button = tk.Button(app, text="Reset", command=reset_game)
reset_button.grid(row=BOARD_SIZE + 4, column=0, columnspan=BOARD_SIZE)

x_turn = tk.BooleanVar()
x_turn.set(True)


app.mainloop()