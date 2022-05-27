from connect4 import Connect4
from bot import Bot
import random

class Interface:
	def __init__(self, nPlayers):
		self.bot = Bot(2)
		self.game = Connect4()
		self.nPlayers = 2
		self.statusText = "No player has made a move yet."
	
	def getGameState(self):
		return self.game.getState()
	
	def generateBotMove(self):
		# move, score = self.bot.minimax_slim(self.game.getState(), True, 6)
		move, score = self.bot.minimax_alphabeta(self.game.getState(), True, 5, self.bot.lossScore, self.bot.winScore)
		return move
	
	def makeBotMove(self):
		if self.game.isPlaying():
			move = self.generateBotMove()
			row, column = move
			markerPosition = self.game.move(column)
			self.setStatusText(self.game.getCurrentPlayer(), markerPosition)
			self.game.switchPlayer()
			return True

		return False
	
	def makeMove(self, column):
		if self.game.isPlaying():
			if self.game.isMoveLegal(column):
				markerPosition = self.game.move(column)
				self.setStatusText(self.game.getCurrentPlayer(), markerPosition)
				self.game.switchPlayer()
			else:
				raise Exception('Move is illegal.')
	
	def makeReplayMove(self):
		move = self.game.makeReplayStep()
		self.setStatusText(self.game.getCurrentPlayer(), move)
		self.game.switchPlayer()

	def handleInput(self, userInput):
		reset = False

		if self.game.isPlaying():
			self.makeMove(userInput)
		elif self.game.hasEnded():
			if userInput == 1:
				self.game.reset()
				self.resetStatusText()
				reset = True
			elif userInput == 2:
				self.game.replayMode() # enter replay mode
		else:
			# step through replay (1) or reset the game (2)
			if userInput == 1:
				self.makeReplayMove()
			elif userInput == 2:
				self.game.reset()
	
		return reset

	def setStatusText(self, player, position):
		self.statusText = 'Player {0} places a marker ({0}) at ({1},{2})'.format(player, position[0], position[1])

		if self.game.hasEnded():
			self.statusText += '\n' + self.getGameEndMessage()
	
	def resetStatusText(self):
		self.statusText = "No player has made a move yet."

	def getStatusText(self):
		return self.statusText

	def getUserInterface(self):
		ui = ''
		ui += '\n' + str(self.getGameState())
		ui += '\n' + self.getStatusText()
		if self.game.hasEnded():
			ui += '\n' + self.getGameEndInstructions()
		if self.game.isReplaying():
			ui += '\n' + self.getReplayStatus()

		return ui

	def getGameEndMessage(self):
		if self.game.hasWinner():
			return 'Player {0} has won!'.format(self.game.getCurrentPlayer())
		else:
			return 'The game ended in a draw.'

	def getGameEndInstructions(self):
		return 'Press 1 to reset the game, 2 to watch a replay of the game.'

	def getReplayStatus(self):
		return 'Watching replay at {0}th move. Press 1 to step through the game or 2 to quit the replay and reset the game.'.format(self.game.replayStep)

	def getInputMsg(self):
		if self.game.isPlaying():
			return 'Choose a column Player {0}: '.format(self.game.getCurrentPlayer())
		elif self.game.hasEnded():
			return 'Game has ended... Choose what to do next: '
		else:
			return 'Replay: Choose what to do next: '
