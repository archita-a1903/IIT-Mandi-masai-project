import os
import random

# Initialize the board and players
def initialize_board():
    return [['-' for _ in range(3)] for _ in range(3)]

def display_board(board):
    print("\nCurrent Board:")
    for row in board:
        print(" | ".join(row))
        print("---+---+---")

def load_game_state():
    if not os.path.exists("game_state.txt"):
        return initialize_board(), 1

    with open("game_state.txt", "r") as file:
        lines = file.readlines()
        board = [line.strip().split(',') for line in lines[:-1]]
        player_turn = int(lines[-1].split(':')[-1].strip())
    return board, player_turn

def check_winner(board):
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != '-':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != '-':
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '-':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '-':
        return board[0][2]

    return None

def is_draw(board):
    return all(cell != '-' for row in board for cell in row)

def make_move(board, position, player):
    row, col = divmod(position - 1, 3)
    if board[row][col] == '-':
        board[row][col] = player
        return True
    print("Invalid move. Please try again.")
    return False

def ai_move(board):
    # AI selects a random empty position
    empty_positions = [(r, c) for r in range(3) for c in range(3) if board[r][c] == '-']
    if empty_positions:
        row, col = random.choice(empty_positions)
        board[row][col] = 'O'

def single_player_mode():
    print("Single Player Mode: You are X. AI is O.")
    board = initialize_board()
    player_turn = 1  # Player starts

    while True:
        display_board(board)
        winner = check_winner(board)
        if winner:
            if winner == 'X':
                print("Congratulations! You win!")
            else:
                print("AI wins. Better luck next time!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        if player_turn == 1:
            move = input("Enter your move (1-9): ").strip()
            if not move.isdigit() or not (1 <= int(move) <= 9):
                print("Invalid input. Please enter a number between 1 and 9.")
                continue

            if make_move(board, int(move), 'X'):
                player_turn = 2
        else:
            print("AI is making a move...")
            ai_move(board)
            player_turn = 1

def two_player_mode():
    print("Two Player Mode")
    board, player_turn = load_game_state()
    players = ['X', 'O']

    while True:
        display_board(board)
        winner = check_winner(board)
        if winner:
            print(f"Player {players.index(winner) + 1} ({winner}) wins!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        print(f"Player {player_turn}, it's your turn ({players[player_turn - 1]}).")
        move = input("Enter your move (1-9) or 'save' to save the game: ").strip()

        if move.lower() == 'save':
            save_game_state(board, player_turn)
            continue

        if not move.isdigit() or not (1 <= int(move) <= 9):
            print("Invalid input. Please enter a number between 1 and 9.")
            continue

        if make_move(board, int(move), players[player_turn - 1]):
            player_turn = 3 - player_turn

def main():
    print("Welcome to Tic Tac Toe!")
    print("1. Single Player Mode")
    print("2. Two Player Mode")

    choice = input("Select mode (1 or 2): ").strip()
    if choice == '1':
        single_player_mode()
    elif choice == '2':
        two_player_mode()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
