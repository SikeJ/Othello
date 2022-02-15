###########################################################################################
# Name: Jackson Sikes
# CWID: 10260611
# Date: 11/15/21
# Description: This is a program in which you can play the Othello game against an AI
###########################################################################################

#importing different libraries to help out with stuff
import random
import sys
import os
import regex as re
import time
import copy
import time

#Sets up a class for the game
class Othello:
	def __init__(self):
		self.board = []
		self.newBoard()
		self.first = "IDK"
		self.player = ' '
		self.player2 = ' '
		self.ai = ' '
		self.players = {}
		self.score = {'X':2, 'O':2}
		self.stackTrace = []
		self.depth = 3
		self.alphaPrune = True
		self.debug = False
		self.clearScreen()
		self.startup(False)

	#Clears the console screen
	def clearScreen(self):
		os.system('cls' if os.name == 'nt' else 'clear')

	#Shows the startup menu of the game & allows the user to pick what they want to do
	def startup(self, error):
		print("Welcome to Othello!")
		print("Would you like to:")
		print("[A] Play a game against another human")
		print("[B] Play the game against the machine")
		print("[C] Load a previously played game")
		print("[Q] To quit the game")

		#Only shows when the user didn't provide a proper input
		if(error):
			print("Looks like you must've mistyped something... try again")

		chose = input("Chose Option: ").lower()
		if(chose == 'a'):
			self.clearScreen()
			self.setPlayers("Player 2")

		elif(chose == 'b'):
			self.clearScreen()
			self.setPlayers("AI")

		elif(chose == 'c'):
			self.clearScreen()
			self.loadGame()

		elif(chose == 'q'):
			self.clearScreen()
			print("Thanks for playing Othello!")
			sys.exit()

		#If the user didn't provide a proper input... ask them again
		else:
			self.clearScreen()
			self.startup(True)
	
	#Method for setting up playing the game against a human or AI
	def setPlayers(self, player):
		self.clearScreen()

		print("Time to play Othello! But before we begin...")
		print("Do you want to go first? (Y/n)")
		goFirst = input().lower()

		#Set's up the players in order to keep track of the turns
		if(goFirst == 'y'):
			self.players = {'X':"Player 1", 'O':player}
			self.player = 'X'
			self.player2 = 'O'

		else:
			self.players = {'O':"Player 1", 'X':player}
			self.player = 'X'
			self.player2 = 'O'

		print(f"Player 1 is {self.player} & {player} is {self.player2}")
		print(f"Therefor {self.players['X']} goes first.")
		time.sleep(1)

		#Starts the game playing against the computer & another human based on what was chosen
		self.playGame()

	#Allows for multiple functtions to determine if the game is at an EOG state
	def gameOver(self):
		return self.score['X'] + self.score['O'] < 64 and self.score['X'] != 0 and self.score['O'] != 0

	#Plays the Othello against another human
	def playGame(self):
		self.resetBoard()
		#Defines the turns of each player
		turns = [self.players['X'], self.players['O']]
		indexT = 0
		noMoves = 0
		while(self.gameOver() and noMoves < 2):
			indexT %= 2

			if(indexT == 0):
				tile = 'X'
			else:
				tile = 'O'

			self.clearScreen()
			self.printBoard()
			moves = self.possibleMoves('X' if indexT == 0 else 'O')

			#If a player has no possible moves, their turn is skipped
			if(len(moves) == 0):
				noMoves += 1
				print(f"Sorry {turns[indexT]}, you aren't able to make any moves so your turn is skipped...")
				input("Press enter to continue.")
				self.stackTrace.append(None)

			else:
				noMoves = 0
				#Allows to seperate the AI from just two people playing
				if(turns[indexT] == "AI"):

					#Allows user to change the depth or enable alpha pruning if they would like				
					self.clearScreen()
					self.printBoard()
					print(f"It's the computer's turn to place a {'X' if indexT == 0 else 'O'} tile on the board...")
					print(f"Current stats: depth:{self.depth} pruning:{self.alphaPrune} debug:{self.debug}")

					good = input("Do you want to change either of these stats? (Y/n) ").lower()
					
					if(good == 'y' or good == 'yes'):
						changeDepth = input("Do you want to change the depth? (Enter an int if so,  "\
											+ "anything else otherwise)\nChange to: ")
						
						#Tries to change the provided string to a number
						try:
							self.depth = int(changeDepth)

						except ValueError:
							pass
						
						#Changes whether to prune or to debug
						changePrune = input("Do you want to enable alphaPruning? (Y,n, or 'Enter' to skip)\nEnable: ").lower()
						if(changePrune == 'y' or changePrune == 'yes'):
							self.alphaPrune = True
						elif(changePrune != ""):
							self.alphaPrune = False

						changeDebug = input("Do you want to print all of the moves with their hueristic values? (Y,n, or 'Enter' to skip)\nDebug: ").lower()
						if(changeDebug == 'y' or changeDebug == 'yes'):
							self.debug = True
						elif(changeDebug != ""):
							self.debug = False

					#Prints how many different possibilities the computer looked at
					xCord, yCord, num = self.makeComputerMove('X' if indexT == 0 else 'O')
					print(f"The AI looked through {num} possible moves, and chose {chr(xCord+ord('A'))}{yCord+1}")
					input("Press 'Enter' to continue")

				else:
					#If it's not the AI's turn it acts normally
					print(f"It is {turns[indexT]}'s ({'X' if indexT == 0 else 'O'}) turn...")
					moveTo = input("Type 'Quit' to quit,\nOr the location you want to place a tile (Ex. A5)\n" \
									+ "Place Tile at: ").lower()
					
					if(moveTo == 'quit'):
						break

					#Ensures that the chosen move is a proper one
					xCord, yCord = self.regexCheck(moveTo)

					#print(xCord)
					#print(yCord)
					#Checks to make sure the provided move is a viable one
					xCord, yCord = self.validMove(xCord, yCord, tile)
				
				#Stores the move into the stackTrace and flips the appropriate tiles
				self.stackTrace.append(f"{xCord}{yCord}")
				self.flipTiles(xCord, yCord, tile, computer=False)
				
			indexT += 1
		
		#Clears the screen in order to show the winning game board
		self.clearScreen()
		self.printBoard()
		print("The game has concluded....")
		if(self.score['X'] > self.score['O']):
			winner = turns[0]
			print(f"The winner was {winner}, with a score of {self.score['X']}-{self.score['O']}")

		elif(self.score['O'] > self.score['X']):
			winner = turns[1]
			print(f"The winner was {winner}, with a score of {self.score['O']}-{self.score['X']}")

		else:
			winner = None
			print(f"The game concluded with a {self.score['X']}-{self.score['O']} draw...")

		#Gives an option to save the stacktrace from the game or return to the main menu
		save = input("Would you like to save the stacktrace of this game? (Y/n) ").lower()
		if(save == 'y' or save == 'yes'):
			self.saveGame(winner)
		restart = input("Would you like to return to the menu? (Y/n) ")
		if(restart == 'y' or restart == 'yes'):
			self.clearScreen()
			self.startup(False)
		else:
			self.clearScreen()
			print("Thanks for playing Othello!")
	
	#Returns all of the possible moves in a list
	def possibleMoves(self, tile, board = []):
		#Creates an empty board
		tempBoard = []
		for i in range(8):
			tempBoard.append([' ']*8)

		if(board == []):
			tempBoard = list(self.board)

		else:
			#Fills the empty board by using the provided board in order to not change anything
			for x in range(8):
				for y in range(8):
					tempBoard[x][y] = board[x][y]

		if(tile == 'X'):
			otherT = 'O'
		elif(tile == 'O'):
			otherT = 'X'

		#Array to keep the directions in which to check for the other tiles
		directions = [[0,1], [1,0], [1,1], [0,-1], [-1,0], [-1,1], [1,-1], [-1,-1]]

		movesList = []
		
		#Loops through the temp board to find all of the possible moves for the given tile
		for xInitial in range(8):
			for yInitial in range(8):
				
				if(tempBoard[xInitial][yInitial] == tile):
					#Step through each direction
					for xDir, yDir in directions:
						x, y = xInitial, yInitial
						x += xDir
						y += yDir

						#As long as the current tile is on the board and the other tile
						if(self.isOnBoard(x, y) and tempBoard[x][y] == otherT):
							#Finds all of the other tiles in this direction
							while(self.isOnBoard(x, y) and tempBoard[x][y] == otherT):
								x += xDir
								y += yDir
							
							#If the current location is an empty spot, it is a valid move
							if(self.isOnBoard(x,y) and tempBoard[x][y] == ' '):
								movesList.append(f"{x}{y}")
			
		movesList = list(set(movesList))
		
		return movesList

	#Provides a function that performs minimax
	def minimax(self, tile, board, depth, maxPlayer, debug):
		movesAvailable = self.possibleMoves(tile, board)
		#print(movesAvailable)
		tempBoard = board.copy()
		num = 0
		#Checks the depth, end of game state, and see's if there's any possible move
		if(depth == 0 or len(movesAvailable) == 0):
			#Returns the current score for the tile of the computer, and the number of checks
			return self.getScore(board)[1 if tile == 'X' else 0], 0, 0, 0

		random.shuffle(movesAvailable)
		#Maximizes for the given tile
		if(maxPlayer):
			maxEval = 0
			maxX = 0
			maxY = 0
			for move in movesAvailable:
				#print(f"Maximizing: {tile}")
				#Takes in the move that is being accounted for
				xS = int(move[0])
				yS = int(move[1])

				#Copies the temporary board into another board to not mess with the memory locations & flips the appropriate tiles
				moveBoard = copy.deepcopy(tempBoard)
				moveBoard = self.flipTiles(xS, yS, tile, moveBoard)
				num += 1

				#Evaluates the next depth with the correct tile
				eval, x, y, check = self.minimax('O' if tile == 'X' else 'X', moveBoard, depth - 1, False, debug)
				
				#Shows the move and the hueristic associated with the move if debugging is enabled
				if(debug):
					print(f"Move: {chr(xS+ord('A'))}{yS+1} Value:{eval}")
				
				num += check
				
				#Ensures the maxEval value is used
				if(eval > maxEval):
					#print(f"Max: {eval}: {xS,yS}")
					maxEval, maxX, maxY = eval, xS, yS
			#returns the eval, and the move that get's that eval, and the number of options evaluated
			return maxEval, maxX, maxY, num
	
		else:
			minEval = 100
			minX = 0
			minY = 0
			for move in movesAvailable:
				#print(f"Minimizing: {tile}")
				#Accounts for the current move
				xS = int(move[0])
				yS = int(move[1])
				#Copies the contents of the board, but not the memory location
				moveBoard = copy.deepcopy(tempBoard)
				moveBoard = self.flipTiles(xS, yS, tile, moveBoard)
				num += 1

				#Evaluates the next depth with the appropriate tile
				eval, x, y, check = self.minimax('X' if tile == 'O' else 'O', moveBoard, depth - 1, True, debug)
				
				if(debug):
					print(f"Move: {chr(xS+ord('A'))}{yS+1} Value:{eval}")
				
				num += check
				#Ensures the minimum hueristic is found and used
				if(eval < minEval):
					#print(f"Min: {eval}: {xS,yS}")
					minEval, minX, minY = eval, xS, yS
			#returns the eval and move to get to that eval, with the number of options evaluated
			return minEval, minX, minY, num

	#Implements the alpha-beta pruning, essentially the same as the minimax function
	def alphaPruning(self, tile, board, depth, alpha, beta, maxPlayer, debug):
		movesAvailable = self.possibleMoves(tile, board)
		tempBoard = board.copy()
		num = 0
		#Checks the depth, end of game state, and see's if there's any possible move
		if(depth == 0 or len(movesAvailable) == 0):
			#Returns the score of the tile that the computer is, and misc options
			return self.getScore(board)[1 if tile == 'X' else 0], 0, 0, 0

		random.shuffle(movesAvailable)
		#Maximizes the result
		if(maxPlayer):
			maxEval = 0
			maxX = 0
			maxY = 0
			for move in movesAvailable:
				xS = int(move[0])
				yS = int(move[1])
				num += 1
				moveBoard = copy.deepcopy(tempBoard)
				moveBoard = self.flipTiles(xS, yS, tile, moveBoard)
				#print(tempBoard)
				#print(moveBoard)
				eval, x, y, check = self.alphaPruning('O' if tile == 'X' else 'X', moveBoard, depth - 1, \
														alpha, beta, False, debug)
				num += check

				#Prints the value associated with the move
				if(debug):
					print(f"Move: {chr(xS+ord('A'))}{yS+1} Value:{eval}")
				
				#Pulls the max value for the alpha, and eval values
				alpha = max(eval, alpha)
				if(eval > maxEval):
					#print(f"Max: {eval}: {xS,yS}")
					maxEval, maxX, maxY = eval, xS, yS

				#If the best option, alpha, is better then the worst, beta, break
				if beta <= alpha:
					break
			#Returns the maxEval and position
			return maxEval, maxX, maxY, num

		#Minimizes the result
		else:
			minEval = 100
			minX = 0
			minY = 0
			for move in movesAvailable:
				#print(f"Minimizing: {tile}")
				xS = int(move[0])
				yS = int(move[1])
				num += 1
				moveBoard = copy.deepcopy(tempBoard)
				moveBoard = self.flipTiles(xS, yS, tile, moveBoard)
				eval, x, y, check = self.alphaPruning('X' if tile == 'O' else 'O', moveBoard, depth - 1, \
														alpha, beta, True, debug)
				#Prints the value associated with the minimizing
				if(debug):
					print(f"Move: {chr(xS+ord('A'))}{yS+1} Value:{eval}")
				num += check
				beta = min(beta, eval)
				if(eval < minEval):
					#print(f"Min: {eval}: {xS,yS}")
					minEval, minX, minY = eval, xS, yS
				if beta <= alpha:
					break
			return minEval, minX, minY, num

	#Starts the AI chosing where to move
	def makeComputerMove(self, tile):
		#Makes an empty board
		tempBoard = []
		for i in range(8):
			tempBoard.append([' ']*8)

		#Sets the current board into
		for x in range(8):
			for y in range(8):
				tempBoard[x][y] = self.board[x][y]

		if(self.depth == 0):
			self.depth = 1

		#Differentiates between alphapruning & non pruning
		if(self.alphaPrune):
			eval, x, y, num = self.alphaPruning(tile, tempBoard, self.depth, float('-inf'), float('inf'), True, self.debug)

		else:
			eval, x, y, num = self.minimax(tile, tempBoard, self.depth, True, self.debug)

		#print(f"The computer is the {tile}")
		#print(f"The computer looked at {num} cases")
		#input()
		return x, y, num

	#Error checks the inputs for the board
	def regexCheck(self, test):
		match = bool(re.fullmatch("[a-h][1-8]", test))

		while(not match):
			print("Not a valid location in the game...")
			test = input("Please select a valid row [A-H] or column [1-8] (Ex. A6): ").lower()
			match = bool(re.fullmatch("[a-h][1-8]", test))
		
		#Takes the coordinates out of the string & returns them
		xCord = int(ord(test[0]) - ord('a'))
		yCord = int(test[1]) - 1
		return xCord, yCord

	#Ensures that the move provided will flip tiles, and flips them if it does
	def flipTiles(self, xStart, yStart, tile, board=[], computer=True):
		#Sets the scope of the current tiles
		if(tile == 'X'):
			otherT = 'O'
		else:
			otherT = 'X'

		if(board == []):
			board = self.board

		#Array to keep the directions in which to check for the other tiles
		directions = [[0,1], [1,0], [1,1], [0,-1], [-1,0], [-1,1], [1,-1], [-1,-1]]

		#Are there any tiles flipped
		flipped = False
		#Checks every direction
		for xDir, yDir in directions:
			x, y = xStart, yStart
			x += xDir
			y += yDir

			#Makes sure that the tile is still on the board
			if(self.isOnBoard(x, y)):
				#Makes sure that there is an enemy tile in the direction
				if(board[x][y] == otherT):
					x += xDir
					y += yDir

					#Loops until a blank or friendly tile is reached
					while(self.isOnBoard(x, y) and board[x][y] == otherT):
						x += xDir
						y += yDir

					#Making sure that the tile is still on the board
					if(self.isOnBoard(x, y)):
						#Checks to see if the tile is a friendly tile
						if(board[x][y] == tile):
							flipped = True
							#Re-loops through the tiles and flips everything
							while(True):
								x -= xDir
								y -= yDir
								board[x][y] = tile
								
								if(x == xStart and y == yStart):
									break

		#If a player selects a move that doesn't flip any tiles, ask them for a move that does
		if(not flipped and not computer):
			print("Sorry, your move is invalid since it can't flip any tiles...")
			newMove = input("Chose a move that sandwhich's your opponents tile: ")
			xCord, yCord = self.regexCheck(newMove)
			xCord, yCord = self.validMove(xCord, yCord, tile)
			self.flipTiles(xCord, yCord, tile)
		return board
							
	#Checks to make sure the location of the move is empty
	def validMove(self, xCord, yCord, tile):
		#print(f"X:{xCord}, Y:{yCord}")
		if(self.board[xCord][yCord] != ' '):
			print(f"The location {chr(xCord + ord('A'))}{yCord+1} is taken up by an {self.board[xCord][yCord]}...")
			string = input("Please select an empty square: ")
			xCord, yCord = self.regexCheck(string)
			xCord, yCord = self.validMove(xCord,yCord, tile)
		return xCord, yCord

	#Ensures that the wanted move is located on the board
	def isOnBoard(self, x, y):
		return x >= 0 and x <= 7 and y >= 0 and y <= 7

	#Saves the stacktrace of the game to a file
	def saveGame(self, winner):
		filename = winner + " " + time.strftime("%H-%M-%S %Y-%m-%d") + '.csv'
		with open(filename, 'w') as saved:
			saved.write(f"{self.players['X']},{self.players['O']}\n")

			while(len(self.stackTrace) != 0):
				saved.write(f"{self.stackTrace.pop(0)},")

	#Method for loading previously saved game
	def loadGame(self):
		self.resetBoard()
		#Reads all of the csv files to find the traces saved in the directory
		files = os.listdir()
		csvFiles = list(filter(lambda f: f.endswith('.csv'), files))

		print("Select the file you want to show:")
		for i, name in enumerate(csvFiles):
			print(f"{i}: {name}")
		#Makes sure that people are selecting a proper file
		while(True):
			chosen = input("Pick file: ")
			try:
				chosen = int(chosen)
				if(chosen >=0 and chosen < len(csvFiles)):
					break
			except ValueError:
				pass
			print("Please pick one of the options...")

		#Set's up the players turns for the given game
		moveTrace = open(csvFiles[chosen], 'r').read().split('\n')
		players = moveTrace[0].split(',')
		moves = moveTrace[1].split(',')
		self.players['X'] = players[0]
		self.players['O'] = players[1]
		turns = [players[0], players[1]]
		indexT = 0

		#Loops through the entire game showing what happen
		while(len(moves) != 1):
			#Keeps up with what tile's turn it was
			indexT %= 2
			if(indexT == 0):
				tile = 'X'
			else:
				tile = 'O'

			#clears the screen and prints the board
			self.clearScreen()
			self.printBoard()
			move = moves.pop(0)
			if(move == 'None'):
				print(f"{turns[indexT]} had their turn skipped since they couldn't make any moves...")

			else:
				x = int(move[0])
				y = int(move[1])
				print(f"{turns[indexT]} chose to place a tile at {chr(x+ord('A'))}{y+1}...")
				self.flipTiles(x, y, tile)

			input("Press 'Enter' to continue")
			indexT += 1

		#Displays the winner of the game
		self.clearScreen()
		self.printBoard()
		print("The game has concluded....")
		if(self.score['X'] > self.score['O']):
			winner = turns[0]
			print(f"The winner was {winner}, with a score of {self.score['X']}-{self.score['O']}")

		elif(self.score['O'] > self.score['X']):
			winner = turns[1]
			print(f"The winner was {winner}, with a score of {self.score['O']}-{self.score['X']}")

		else:
			winner = None
			print(f"The game concluded with a {self.score['X']}-{self.score['O']} draw...")
		
		#Gives player to option to return to main menu
		restart = input("Would you like to return to the menu? (Y/n) ")
		if(restart == 'y' or restart == 'yes'):
			self.clearScreen()
			self.startup(False)
		else:
			self.clearScreen()
			print("Thanks for playing Othello!")

	#Ensures that the board has been setup properly
	def newBoard(self):
		self.board = []
		for i in range(8):
			self.board.append([' ']*8)

	#Resets the game playing board
	def resetBoard(self):
		#Clearing the board for the game
		for x in range(8):
			for y in range(8):
				self.board[x][y] = ' '

		self.score['X'] = 2
		self.score['O'] = 2

		#Setting the starting pieces for the game
		self.board[4][4] = 'O'
		self.board[3][3] = 'O'
		self.board[3][4] = 'X'
		self.board[4][3] = 'X'

	#Prints the current state of the board
	def printBoard(self):
		print(" | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |")
		print("-"*34)

		self.getScore()

		#Prints the layout for the board with the actual values on the inside so far
		for i, col in enumerate(self.board):
			s = f"{chr(ord('A')+i)}"
			for row in self.board[i]:
				s += f"| {row} "
			s += "|"
			print(s)
			print("-"*34)

		print(f"The score is: X:{self.score['X']} O:{self.score['O']}")

	#Gets the current score of the game
	def getScore(self, board=[]):
		#Calculates the score based on the current state of the board
		if(board == []):
			board = list(self.board)

			self.score['X'] = 0
			self.score['O'] = 0

			#Loops through the board adding the score for each tile
			for x in range(8):
				for y in range(8):
					tile = board[x][y]
					if(tile == 'X'):
						self.score['X'] += 1

					elif(tile == 'O'):
						self.score['O'] += 1
		
		#Else calculates and returns the scores of any board state
		else:
			#print(board)
			xTile = oTile = 0
			for x in range(8):
				for y in range(8):
					if(board[x][y] == 'X'):
						xTile += 1

					elif(board[x][y] == 'O'):
						oTile += 1
			
			return xTile, oTile

if __name__ == "__main__":
	game = Othello()
