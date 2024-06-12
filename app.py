from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def print_board(board):
    return "\n".join([" | ".join(row) + "\n" + "-" * 5 for row in board])

def check_winner(board, player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        row = int(request.form['row'])
        col = int(request.form['col'])

        if board[row][col] != " ":
            return jsonify({'status': 'error', 'message': 'That position is already taken. Try again.'})

        board[row][col] = current_player

        if check_winner(board, current_player):
            return jsonify({'status': 'win', 'message': f'Player {current_player} wins!', 'board': print_board(board)})
        elif is_board_full(board):
            return jsonify({'status': 'tie', 'message': "It's a tie!", 'board': print_board(board)})

        current_player = "O" if current_player == "X" else "X"

@app.route('/reset', methods=['POST'])
def reset():
    return jsonify({'status': 'success'})

if __name__ == "__main__":
    app.run(debug=True)
