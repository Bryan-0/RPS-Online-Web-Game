#!/usr/bin/env python3
from flask import Flask, render_template, Response, request, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, send, emit

app = Flask(__name__, static_url_path='/templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

players = []
moveList = []

@app.route("/")
def index():
	return render_template("lobby.html")

@app.route('/files/<path:filename>')
def send_file(filename):
    return send_from_directory('js', 'game.js')

@app.route("/script", methods=['GET'])
def script():
	return app.send_static_file('static/game.js')

@app.route("/lobby", methods=['POST', 'GET'])
def lobby():
	return redirect(url_for('index'))

@app.route("/match", methods=['POST', 'GET'])
def game():
	if request.method == 'GET':
		return f"<center><h1><strong>ERROR: Please don't load this page directly.</strong></h1></center>"

	#players.append(request.form['userNameInput'])
	return render_template("game.html")

# Sockets
@socketio.on('addPlayer')
def addPlayer():
	players.append(request.sid)
	print('Players: ')
	print(players)
	print()

@app.route("/thanks", methods=['POST'])
def removePlayer():
	try:
		players.pop()
	except:
		pass
	print('Players: ')
	print(players)
	print()
	socketio.emit('playersNOTOnline', broadcast=True)
	return "<style> body { background-color: black; } h1 { color: green; font-size: 50px; } button { border-radius: 6px; background-color: #53a2be; font-size: 35px; } #thanks { margin-top: 300px; }</style><center><div id=\"thanks\"><h1>Thanks for playing :]</h1><p></p><form action=\"/lobby\" method=\"POST\"><button type=\"submit\"> Lobby </button></form></div></center>"

@socketio.on('checkPlayers')
def checkPlayers():
	if len(players) >= 2:
		emit('playersOnline', broadcast=True)

@socketio.on('disconnect')
def leaveGame():
	try:
		players.remove(request.sid)
		print('Players: ')
		print(players)
		print()
	except:
		pass
	emit('playersNOTOnline', broadcast=True)

# Game sockets
@socketio.on('playerMove')
def playerMove(playerOption):
	moveList.append(playerOption)
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
	for move in moveList:
		moveList.remove(move)
	emit('showWinner', winner, broadcast=True)

@socketio.on('Tied')
def whoWon():
	print("The match is tied!")
	for move in moveList:
		moveList.remove(move)
	emit('showTied', broadast=True)

@socketio.on('playAgain')
def playAgain():
	emit('restartGame', broadcast=True)

if __name__ == '__main__':
	socketio.run(app, debug=True)