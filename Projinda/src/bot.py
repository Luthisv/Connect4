from connect4 import Connect4
import math
import numpy as np

class Bot:
	
	def __init__(self, playerID):
		self.winScore = math.inf  # The score a move gets if it wins the game
		self.drawScore = 0  # The score of a move if it get
		self.lossScore = -math.inf  # The score of a move that results in a loss
		self.playerID = playerID
		self.opposingPlayer = playerID ^ 3
        
	def minimax_slim(self, state, maximizingPlayer, depth):
		"""
		:param depth: how many moves deeper the algorithm should continue, it stops at depth 0
		:param move: which column this turn's marker will be put
		:param maximizingPlayer: true if it the turn of the player who wants to maximize the score
		:param state: the current game state
		:return: move and score
		"""
		player = self.playerID if maximizingPlayer else self.opposingPlayer

		if depth == 0:
			x = Connect4.staticScore(state, self.playerID)
			return (None, x)
		
		# add more base cases
		legalMoves = Connect4.staticLegalMovesFromState(state)
		bestScore = self.lossScore if maximizingPlayer else self.winScore
		bestMove = None
		for move in legalMoves:
				# copy = np.copy(state)
				copy = Connect4.staticStateAfterMove(state, move, player)
				isWinningMove = Connect4.staticIsWinningMove(copy, move)
				if isWinningMove:
					if maximizingPlayer:
						return (move, self.winScore)
					else:
						return (move, self.lossScore)


				discard, score = self.minimax_slim(copy, not maximizingPlayer, depth-1)
				if maximizingPlayer and score > bestScore:
						bestScore = score
						bestMove = move

				elif not maximizingPlayer and score < bestScore:
						bestScore = score
						bestMove = move
 
		return (bestMove, bestScore)

	def minimax_alphabeta(self, state, maximizingPlayer, depth, alpha, beta):
		player = self.playerID if maximizingPlayer else self.opposingPlayer

		if depth == 0:
			x = Connect4.staticScore(state, self.playerID)
			return (None, x)
		
		# add more base cases
		legalMoves = Connect4.staticLegalMovesFromState(state)
		bestScore = self.lossScore if maximizingPlayer else self.winScore
		bestMove = legalMoves[0] if len(legalMoves) > 0 else None
		for move in legalMoves:
				copy = Connect4.staticStateAfterMove(state, move, player)
				isWinningMove = Connect4.staticIsWinningMove(copy, move)
				# special cases
				if isWinningMove:
					if maximizingPlayer:
						return (move, self.winScore)
					else:
						return (move, self.lossScore)


				temp, score = self.minimax_alphabeta(copy, not maximizingPlayer, depth-1, alpha, beta)
				
				# bestScore = max(score)
				if maximizingPlayer and score > bestScore:
						bestScore = score
						bestMove = move
						alpha = score

				# bestScore = min(score)
				elif not maximizingPlayer and score < bestScore:
						bestScore = score
						bestMove = move
						beta = score
				
				if alpha >= beta:
					break
 
		return (bestMove, bestScore)
