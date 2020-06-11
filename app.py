#!/usr/bin/env python3
from flask import Flask, render_template, Response, request, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, send, emit

app = Flask(__name__, static_url_path='/templates')
app.config['SECRET_KEY'] = 'secret!'
app.config["TEMPLATES_AUTO_RELOAD"] = True
socketio = SocketIO(app)

class GlobalVars():
	def __init__(self):
		print("Started Global Variables")
		self.players = []
		self.moveList = []
		self.playerPoints = {}
		self.movePoints = []

globals_variables = GlobalVars()

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

	globals_variables.players.append(request.form['userNameInput'])
	return render_template("game.html")

# Sockets
@socketio.on('addPlayer')
def addPlayer():
	globals_variables.players.append(request.sid)
	globals_variables.playerPoints[request.sid] = 0
	print('Players: ')
	print(globals_variables.players)
	print(globals_variables.playerPoints)
	print()
	if len(globals_variables.players) == 4:
		emit('PlayerList', [globals_variables.players[2:4], globals_variables.playerPoints], broadcast=True)
		emit('PlayerList', [globals_variables.players[0:2], globals_variables.playerPoints])
	else:
		emit('PlayerList', [globals_variables.players, globals_variables.playerPoints], broadcast=True)

@app.route("/thanks", methods=['POST'])
def exitButtonGame():
	return "<style> body { background-color: black; } h1 { color: green; font-size: 50px; } button { border-radius: 6px; background-color: #53a2be; font-size: 35px; } #thanks { margin-top: 300px; }</style><center><div id=\"thanks\"><h1>Thanks for playing :]</h1><p></p><form action=\"/lobby\" method=\"POST\"><button type=\"submit\"> Lobby </button></form></div></center>"

@socketio.on('checkPlayers')
def checkPlayers():
	if len(globals_variables.players) >= 4:
		emit('playersOnline', broadcast=True)

# Game sockets
@socketio.on('playerMove')
def playerMove(playerOption):
	globals_variables.moveList.append(playerOption)
	globals_variables.movePoints.append(playerOption)
	globals_variables.movePoints.append(request.sid)
	print('Move List: ')
	print(globals_variables.moveList)
	print()

@socketio.on('checkMoves')
def checkMoves():
	if len(globals_variables.moveList) >= 2:
		emit('CheckWinner', globals_variables.moveList[::-1], broadcast=True)

@socketio.on('Winner')
def whoWon(winner):
	print(f"{winner} has won the game!")
	winnerID = globals_variables.movePoints.index(winner) + 1
	globals_variables.playerPoints[str(globals_variables.movePoints[winnerID])] += 1
	for move in globals_variables.moveList:
		globals_variables.moveList.remove(move)
	emit('showWinner', [winner, str(globals_variables.movePoints[winnerID]), globals_variables.playerPoints[str(globals_variables.movePoints[winnerID])]], broadcast=True)
	print(globals_variables.playerPoints)

@socketio.on('Tied')
def whoWon():
	print("The match is tied!")
	for move in globals_variables.moveList:
		globals_variables.moveList.remove(move)
	emit('showTied', broadast=True)

@socketio.on('playAgain')
def playAgain():
	removeID = globals_variables.movePoints.index(request.sid) - 1
	globals_variables.movePoints.pop(removeID)
	globals_variables.movePoints.remove(request.sid)
	emit('restartGame', broadcast=True)

@socketio.on('disconnect')
def leaveGame():
	name = globals_variables.players.index(request.sid)
	globals_variables.players.pop(name - 1)
	globals_variables.players.remove(request.sid)
	del globals_variables.playerPoints[request.sid]
	globals_variables.movePoints = []
	print('Players: ')
	print(globals_variables.players)
	print(globals_variables.playerPoints)
	print(globals_variables.movePoints)
	print()
	emit('playersNOTOnline', broadcast=True)
	emit('removePlayerFromList', request.sid, broadcast=True)

if __name__ == '__main__':
	socketio.run(app, debug=True)