// Game functions

function initialize() {
  socket.emit('addPlayer')
  socket.emit('checkPlayers')
}

function hideAll() {
  statsToHide = ['waitMove', 'gameStarted', 'WinnerStatus', 'TiedStatus']
  for(let i=0; i < statsToHide.length; i++) {
  	document.getElementById(statsToHide[i]).style.display = 'none'
  }
  document.getElementById('waitStatus').style.display = 'block'
}

function showAll() {
	document.getElementById('waitStatus').style.display = 'none'
    document.getElementById('gameStarted').style.display = 'block'
}

function playerMove(playerOption) {
  document.getElementById('gameStarted').style.display = 'none'
  document.getElementById('waitMove').style.display = 'block'
  socket.emit('playerMove', playerOption)
  socket.emit('checkMoves')
}

function checkWinner(firstMove, secondMove) {
  document.getElementById('waitMove').style.display = 'none'

  if (firstMove == 'paper_btn' && secondMove == 'scissor_btn') {
    socket.emit('Winner', secondMove)
  } else if (firstMove == 'scissor_btn' && secondMove == 'paper_btn') {
    socket.emit('Winner', firstMove)
  } else if (firstMove == 'scissor_btn' && secondMove == 'rock_btn') {
    socket.emit('Winner', secondMove)
  } else if (firstMove == 'rock_btn' && secondMove == 'scissor_btn') {
    socket.emit('Winner', firstMove)
  } else if (firstMove == 'rock_btn' && secondMove == 'paper_btn') {
    socket.emit('Winner', secondMove)
  } else if (firstMove == 'paper_btn' && secondMove == 'rock_btn') {
    socket.emit('Winner', firstMove)
  } else {
    socket.emit('Tied')
  }
}

function showWinner(winner) {
  possibleWinners = {
	'paper_btn': 'https://static.thenounproject.com/png/477922-200.png', 
	'scissor_btn': 'https://static.thenounproject.com/png/88666-200.png',
	'rock_btn': 'https://static.thenounproject.com/png/88661-200.png'
  }

  document.getElementById('winnerimg').src = possibleWinners[winner]
  document.getElementById('WinnerStatus').style.display = 'block'
}

function TiedStatus() {
  document.getElementById('TiedStatus').style.display = 'block'
}

function playAgain() {
  socket.emit('playAgain')
}

function restartGame() {
  statsToHide = ['WinnerStatus', 'TiedStatus']
  for(let i=0; i < statsToHide.length; i++) {
  	document.getElementById(statsToHide[i]).style.display = 'none'
  }
  document.getElementById('gameStarted').style.display = 'block'
}

function exitGame() {
  socket.emit('checkPlayers')
}