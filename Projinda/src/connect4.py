import numpy as np
import random

"""
The game is represented as a 6x7 matrix of integers.

Each element can hold one of three values:
0 means the slot is empty.
1 means Player 1 has placed a marker there.
2 means Player 2 has placed a marker there.

"""

class Connect4:

  def __init__(self):
    # initialize board
    self.rows = 6
    self.columns = 7
    self.numberOfSlots = self.rows*self.columns
    self.state = np.zeros(self.numberOfSlots).reshape(self.rows, self.columns)

    # Player 1 starts
    self.currentPlayer = 1
    # -1 means no winner
    self.winner = -1 
    self.history = []
    # Game modes: 0 = playing, 1 = ended, 2 = replay-mode
    self.mode = 0
    self.replayStep = 0

  def __str__(self):
    return str(self.state)

  def reset(self):
    # reset the game by calling the init-method
    self.__init__()
  
  # static methods

  @staticmethod
  def getEvaluationMatrix():
    # get the weights of each position in the board
    return np.array([
        [3, 4, 5, 7, 5, 4, 3],
        [4, 6, 8, 10, 8, 6, 4],
        [5, 8, 11, 13, 11, 8, 5],
        [5, 8, 11, 13, 11, 8, 5],
        [4, 6, 8, 10, 8, 6, 4],
        [3, 4, 5, 7, 5, 4, 3]
    ])

  @staticmethod
  def staticFindLastFreeRow(state, row, column):
    # search a column for an empty place to put a marker (from top to bottom)
    if state[row, column] == 0:
      row += 1
      if row < state.shape[0]:
        return Connect4.staticFindLastFreeRow(state, row, column)
    return row - 1

  @staticmethod
  def staticStateAfterMove(state, move, player):
    # Return a copy of the state with a disk added to it
    row, column = move
    copy = np.copy(state)
    copy[row, column] = player
    return copy
  
  @staticmethod
  def staticScore(state, player):
    # calculate score difference between two players
    weights = Connect4.getEvaluationMatrix()
    playerState = state == player
    opponentState = state == (player ^ 3)

    playerState = playerState.astype(int)
    opponentState = opponentState.astype(int)

    playerScore = np.sum(np.multiply(weights, playerState))
    opponentScore = np.sum(np.multiply(weights, opponentState))

    return playerScore - opponentScore

  @staticmethod
  def staticIsWinningMove(state, move):
    # check if a move resulted in a victory
    streaks = Connect4.staticScoreFromMove(state, move)
    longestStreak = max(streaks)
    return longestStreak >= 4

  @staticmethod
  def staticLegalMovesFromState(state):
    # find all legal moves (columns where a disk can be placed), given a specific state
    legalMoves = []
    for column in range(state.shape[1]): # shape returns (height, width)
      if state[0, column] == 0:
        row = Connect4.staticFindLastFreeRow(state, 0, column)
        legalMoves.append((row, column))
    return legalMoves
  
  @staticmethod
  def staticScoreFromMove(state, move):
    # check how many disks there are in a row
    # in each possible path
    row, column = move
    scores = []
    connected = Connect4.staticGetAllConnected(state, row, column)
    indexes = Connect4.staticGetIndexes(state, row, column)

    for i in range(len(connected)):
      scores.append(Connect4.staticNInARow(connected[i], indexes[i]))
    return tuple(scores)

  @staticmethod
  def staticGetAllConnected(state, row, column):
    # return arrays representing the different paths one disk is connected to
    connectedRow = Connect4.staticRow(state, row)
    connectedCol = Connect4.staticColumn(state, column)
    connectedDiagDesc = Connect4.staticDescDiag(state, row, column)
    connectedDiagAsc = Connect4.staticAscDiag(state, row, column)
    
    return (connectedRow, connectedCol, connectedDiagDesc, connectedDiagAsc)

  @staticmethod
  def staticGetIndexes(state, row, column):
    # get indexes for the disk at (row, column) in the arrays returned from staticGetAllConnected
    return (column, row, min(column, row), min(state.shape[1] - column - 1, row))

  @staticmethod
  def staticRow(state, row):
    # get an array representing one row of the board
    return state[row, :]

  @staticmethod
  def staticColumn(state, column):
    # get an array representing one column of the board
    return state[:, column]

  @staticmethod
  def staticAscDiag(state, row, column):
    # get an array representing the ascending diagonal that intersects the position (row, column)
    diagOffsetAsc = state.shape[1] - column - 1 - row
    connectedDiagAsc = np.fliplr(state).diagonal(diagOffsetAsc)
    return connectedDiagAsc

  @staticmethod
  def staticDescDiag(state, row, column):
    # get an array representing the descending diagonal that intersects the position (row, column)
    diagOffsetDesc = column - row
    connectedDiagDesc = state.diagonal(diagOffsetDesc)
    return connectedDiagDesc
  
  @staticmethod
  def staticNInARow(arr, index):
    # count the number of equal elements in a row in an array
    # this is used to check if a player's move resluted in a victory
    player = arr[index]
    length = len(arr)
    counter = 1
    temp = index+1
    while temp < length and arr[temp] == player:
      counter += 1
      temp += 1

    temp = index-1
    while temp >= 0 and arr[temp] == player:
      counter += 1
      temp -= 1

    return counter

  # end static methods

  def replayMode(self):
    # enter replay mode
    self.mode = 2
    self.winner = -1
    self.replayStep = 0
    self.state = np.zeros(self.numberOfSlots).reshape(self.rows, self.columns)
    self.currentPlayer = 1

  def makeReplayStep(self):
    # game class probably shouldn't have this
    # this is used to replay a game from history
    col = self.history[self.replayStep]
    row = self.findLastFreeRow(self.rows-1, col)
    self.move(col)
    self.replayStep += 1
    return (row, col)

  def calcScoreFromMove(self, row, column):
    return Connect4.staticScoreFromMove(self.getState(), (row, column))

  def isMoveLegal(self, column):
    return self.findLastFreeRow(0, column) != -1

  def move(self, column):
    # Current player makes a move
    # returns position where the disk landed (row, column)
    markerRow = self.findLastFreeRow(0, column)
    self.state[markerRow, column] = self.currentPlayer
    self.history.append(column)
    if self.isGameWinningMove(markerRow, column):
      self.setWinner(self.currentPlayer)
    self.updateGameMode()

    return (markerRow, column)

  def switchPlayer(self):
    # change player from 1 to 2, or from 2 to 1
    self.currentPlayer ^= 3

  def endGame(self):
    # end the game
    self.mode = 1

  def updateGameMode(self):
    # game has a winner or the board is full means the game has ended
    if self.hasWinner() or self.isBoardFull():
      self.endGame()
  
  def isBoardFull(self):
    # check if the board is full of disks
    return np.count_nonzero(self.state) == self.numberOfSlots

  def isGameWinningMove(self, row, column):
    return Connect4.staticIsWinningMove(self.getState(), (row, column))

  def findLastFreeRow(self, row, column):
    return Connect4.staticFindLastFreeRow(self.getState(), row, column)

  def setWinner(self, player):
    self.winner = player

  def getState(self):
    return self.state

  def getCurrentPlayer(self):
    return self.currentPlayer

  def hasEnded(self):
    return self.mode == 1

  def isPlaying(self):
    return self.mode == 0

  def isReplaying(self):
    return self.mode == 2

  def getGameMode(self):
    return self.mode

  def hasWinner(self):
    # check if the game has a winner
    return self.winner != -1

  def getAllConnected(self, row, column):
    return Connect4.staticGetAllConnected(self.getState(), row, column)

  def getIndexes(self, row, column):
    return Connect4.staticGetIndexes(self.getState(), row, column)

  def getRow(self, row):
    return Connect4.staticRow(self.getState(), row)

  def getColumn(self, column):
    return Connect4.staticColumn(self.getState(), column)

  def getAscDiag(self, row, column):
    return Connect4.staticAscDiag(self.getState(), row, column)

  def getDescDiag(self, row, column):
    return Connect4.staticDescDiag(self.getState(), row, column)

  def getWinner(self):
    return self.winner

  def getMode(self):
    return self.mode
  
  def getRows(self):
    return self.rows

  def getColumns(self):
    return self.columns
