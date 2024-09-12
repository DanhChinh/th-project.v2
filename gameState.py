import copy
import numpy
from rule import get_all_valid_moves, get_valid_moves


class gameState:
	def __init__(self,pieces, turn, history=[]):
		self.pieces = pieces
		self.turn = turn
		self.undoPs = None
		self.player_valid_moves = {}
		self.history = history
		self.done = False
		# print("history", len(self.history))
	def show(self):
		for i in range(10):
			for j in range(9):
				text = str('+').center(7)
				if (i, j) in self.pieces:
					text = str(self.pieces[(i,j)]['name']).center(7)
				print(text, end="")
			print()
	def move(self,move):
		history = []
		(fi, fj, ti, tj) = move
		if (fi,fj) not in self.pieces:
			print("Vi tri khong kha dung")
			print(self.pieces)
			print(move)
			import sys
			# sys.exit()
		self.pieces[(ti, tj)] = self.pieces[(fi, fj)]
		del self.pieces[(fi, fj)]
		if self.turn == "black":
			self.turn = "red"
		else:
			self.turn = "black"
		return self


	def makeChild(self, move):
		hs = str(self.pieces)

		(fi,fj, ti,tj) = move
		pieces = copy.deepcopy(self.pieces)
		piece_remove = pieces.pop((fi,fj))
		pieces[(ti, tj)] = piece_remove
		turn = 'black'
		if self.turn == "black":
			turn = 'red'
		history = copy.deepcopy(self.history)
		history.append(hs)
		return gameState(pieces, turn, history)
	def is_game_over(self):
		scores = self.evaluate_board()
		return scores>5000 or scores<-5000
	def evaluate_board(self):
		scores = {
			"chariot": 50,
			"horse": 35,
			"elephant": 20,
			"advisor":15,
			"general": 99999,
			"cannon": 30,
			"soldier" :10 
	
		}
		coefficients = {
			"red":-1,
			"black":1
		}

		value = 0
		for (i,j), piece in self.pieces.items():
			if piece["color"] == self.turn:
				value += scores[piece["name"]]
			else:
				value -= scores[piece["name"]]
			# value += scores[piece["name"]] * coefficients[piece["color"]]
		if value > 5000 or value < -5000:
			self. done = True
		return value
	def get_all_valid_moves(self): 
		'''
		return [(x, y, nx, ny), ...]
		'''
		return get_all_valid_moves(self.pieces, self.turn)
	def get_dict_valid_moves(self):
		for (row, col), piece in self.pieces.items():
			if piece['color'] == self.turn:
				self.player_valid_moves[(row, col)] = get_valid_moves(self.pieces, row, col)
	def find_best_move(self, depth):
		best_move = None
		best_value = float('-inf')
		for move in self.get_all_valid_moves():
			child = self.makeChild(move)
			move_value = child.minimax(depth - 1, float('-inf'), float('inf'), False)
			if move_value > best_value:
				best_value = move_value
				best_move = move
		print('best value:', best_value)
		return best_move
	def minimax(self, depth, alpha, beta, maximizing_player):
		if depth == 0 or self.is_game_over():
			return self.evaluate_board()

		stringboard = str(self.pieces)
		if self.history.count(stringboard):
			return -999
		if maximizing_player:
			max_eval = float('-inf')
			for move in self.get_all_valid_moves():
				child = self.makeChild(move)
				eval = child.minimax(depth - 1, alpha, beta, False)
				max_eval = max(max_eval, eval)
				alpha = max(alpha, eval)
				if beta <= alpha:
					break
			return max_eval
		else:
			min_eval = float('inf')
			for move in self.get_all_valid_moves():
				child = self.makeChild(move)
				eval = child.minimax(depth - 1, alpha, beta, True)
				min_eval = min(min_eval, eval)
				beta = min(beta, eval)
				if beta <= alpha:
					break
			return min_eval
def chessman(name, color):
	return {
		"name":name,
		"color":color
	}
def makeInitGameState():
	# board = [   
	# 			['', '','','','general','','','',''],
	# 			['','','','','','','','',''],
	# 			['','','','','','','','',''],
	# 			['','','','','horse','','','',''],
	# 			['','','','','','','','',''],
	# 			['soldier','','','horse','','','','',''],
	# 			['','','','','','','','',''],
	# 			['','','','','','','','',''],
	# 			['','','','','','','','',''],
	# 			['', '','','','chariot','','','','']
	# 		]
	board = [   
				['chariot', 'horse','elephant','advisor','general','advisor','elephant','horse','chariot'],
				['','','','','','','','',''],
				['','cannon','','','','','','cannon',''],
				['soldier','','soldier','','soldier','','soldier','','soldier'],
				['','','','','','','','',''],
				['','','','','','','','',''],
				['soldier','','soldier','','soldier','','soldier','','soldier'],
				['','cannon','','','','','','cannon',''],
				['','','','','','','','',''],
				['chariot', 'horse','elephant','advisor','general','advisor','elephant','horse','chariot']	
			]
	pieces = {}
	for r in range(10):
		for c in range(9):
			if board[r][c]:
				color  = 'black' if r<=4 else'red'
				pieces[(r,c)] = chessman(board[r][c],color)
	firstState = gameState(pieces, "black")
	# print(str(firstState.pieces))
	return firstState

# firstState = makeInitGameState()
