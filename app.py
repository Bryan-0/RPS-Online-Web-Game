#!/usr/bin/env python3
from flask import Flask, render_template, Response, request, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, send, emit

app = Flask(__name__, static_url_path='/templates')
app.config['SECRET_KEY'] = 'secret!'
app.config["TEMPLATES_AUTO_RELOAD"] = True
socketio = SocketIO(app)

players = []
moveList = []
playerPoints = {}
movePoints = []

@app.route("/")
def index():
	return render_template("lobby.html")

@app.route('/files/<path:filename>')
def send_file(filename):
    return send_from_directory('js', 'game.js')

@app.route('/style/<path:filename>')
def send_css_file(filename):
    return send_from_directory('css', 'style.css')

@app.route("/lobby", methods=['POST', 'GET'])
def lobby():
	return redirect(url_for('index'))

@app.route("/match", methods=['POST', 'GET'])
def game():
	if request.method == 'GET':
		return f"<center><h1><strong>ERROR: Please don't load this page directly.</strong></h1></center>"

	players.append(request.form['userNameInput'])
	return render_template("game.html")

# Sockets
@socketio.on('addPlayer')
def addPlayer():
	players.append(request.sid)
	playerPoints[request.sid] = 0
	print('Players: ')
	print(players)
	print(playerPoints)
	print()
	if len(players) == 4:
		emit('PlayerList', [players[2:4], playerPoints], broadcast=True)
		emit('PlayerList', [players[0:2], playerPoints])
	else:
		emit('PlayerList', [players, playerPoints], broadcast=True)

@app.route("/thanks", methods=['POST'])
def exitButtonGame():
	return "<style> body { background-color: black; } h1 { color: green; font-size: 50px; } button { border-radius: 6px; background-color: #53a2be; font-size: 35px; } #thanks { margin-top: 300px; }</style><center><div id=\"thanks\"><h1>Thanks for playing :]</h1><p></p><form action=\"/lobby\" method=\"POST\"><button type=\"submit\"> Lobby </button></form></div></center>"

@socketio.on('checkPlayers')
def checkPlayers():
	if len(players) >= 4:
		emit('playersOnline', broadcast=True)

@socketio.on('disconnect')
def leaveGame():
	try:
		removeID = movePoints.index(request.sid) - 1
		movePoints.pop(removeID)
		movePoints.remove(request.sid)
	except:
		pass
	name = players.index(request.sid)
	players.pop(name - 1)
	players.remove(request.sid)
	del playerPoints[request.sid]
	print('Players: ')
	print(players)
	print(playerPoints)
	print()
	emit('playersNOTOnline', broadcast=True)
	emit('removePlayerFromList', request.sid, broadcast=True)

# Game sockets
@socketio.on('playerMove')
def playerMove(playerOption):
	moveList.append(playerOption)
	movePoints.append(playerOption)
	movePoints.append(request.sid)
	print('Move List: ')
	print(moveList)
	print()

@socketio.on('checkMoves')
def checkMoves():
	if len(moveList) >= 2:
		emit('CheckWinner', moveList[::-1], broadcast=True)

@socketio.on('Winner')
def whoWon(winner):
	print(f"{winner} has won the game!")
	winnerID = movePoints.index(winner) + 1
	playerPoints[str(movePoints[winnerID])] += 1
	for move in moveList:
		moveList.remove(move)
	emit('showWinner', [winner, str(movePoints[winnerID]), playerPoints[str(movePoints[winnerID])]], broadcast=True)
	print(playerPoints)

@socketio.on('Tied')
def whoWon():
	print("The match is tied!")
	for move in moveList:
		moveList.remove(move)
	emit('showTied', broadast=True)

@socketio.on('playAgain')
def playAgain():
	removeID = movePoints.index(request.sid) - 1
	movePoints.pop(removeID)
	movePoints.remove(request.sid)
	emit('restartGame', broadcast=True)

if __name__ == '__main__':
	socketio.run(app, debug=True)