from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'basic_tictactoe_key'  # Needed for session

@app.route("/", methods=["GET", "POST"])
def index():
    if 'board' not in session:
        reset_game()

    message = session.get('message', "X's Turn")
    winner_message = session.get('winner_message', "")
    show_result_dialog = session.get('show_result_dialog', False)

    if request.method == "POST":
        if "start_game" in request.form:
            player_x = request.form.get("name1") or "Player X"
            player_o = request.form.get("name2") or "Player O"
            session['players'] = {'X': player_x, 'O': player_o}
            session['is_game_active'] = True
            session['message'] = f"{player_x}'s Turn"
            session['show_names_dialog'] = False
            reset_game()
        elif "move" in request.form:
            index = int(request.form.get("move"))
            make_move(index)
        elif "reset" in request.form:
            reset_game()

    return render_template("index.html",
                           board=session['board'],
                           message=session['message'],
                           winner_message=session['winner_message'],
                           show_names_dialog=session.get('show_names_dialog', True),
                           show_result_dialog=session.get('show_result_dialog', False),
                           players=session.get('players', {'X': 'Player X', 'O': 'Player O'})
                           )

def reset_game():
    session['board'] = [""] * 9
    session['current_player'] = "X"
    session['is_game_active'] = True
    session['message'] = f"{session.get('players', {'X': 'Player X'})['X']}'s Turn"
    session['winner_message'] = ""
    session['show_result_dialog'] = False
    session['show_names_dialog'] = True

def make_move(index):
    board = session['board']
    if not session['is_game_active'] or board[index] != "":
        return

    board[index] = session['current_player']
    session['board'] = board
    winner = check_winner(board)

    if winner:
        session['is_game_active'] = False
        if winner == "Tie":
            session['winner_message'] = "It's a Tie!"
        else:
            player_name = session['players'][winner]
            session['winner_message'] = f"{player_name} Wins!"
        session['show_result_dialog'] = True
    else:
        next_player = "O" if session['current_player'] == "X" else "X"
        session['current_player'] = next_player
        session['message'] = f"{session['players'][next_player]}'s Turn"

def check_winner(board):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for a, b, c in wins:
        if board[a] and board[a] == board[b] and board[a] == board[c]:
            return board[a]
    return "Tie" if "" not in board else None

if __name__ == "__main__":
    app.run(debug=True, port=5001)