// Game functions

function initialize() {
  socket.emit('addPlayer')
  socket.emit('checkPlayers')
}

/*
function showPlayerList(players) {
  for(let i=0; i < players[0].length; i++) {
    if (i % 2 == 0) {
      var table = document.getElementById("usersTable");
      var row = table.insertRow(1);
      row.setAttribute("id", `${players[0][i+1]}`)
      var cell1 = row.insertCell(0);
      var cell2 = row.insertCell(1);
      cell1.innerHTML = players[0][i];
      cell2.innerHTML = players[1][socket.io.engine.id];
    }
  }
}

function removePlayerList(playerID) {
  var row = document.getElementById(String(playerID));
  row.parentNode.removeChild(row);
}
*/

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

  document.getElementById('winnerimg').src = possibleWinners[winner[0]]
  var row = document.getElementById(winner[1])
  document.getElementById('winnerName').innerHTML = `► ${row.cells.item(0).innerHTML} ◄`
  document.getElementById('WinnerStatus').style.display = 'block'
}

function updateTable(winner) {
  var row = document.getElementById(winner[1])
  if (parseInt(winner[2]) % 2 == 0) {
    row.cells.item(1).innerHTML = parseInt(winner[2] / 2);
  }
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