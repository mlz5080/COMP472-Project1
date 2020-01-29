import numpy as np

class Gameboard():
	alphabet=['A','B','C','D','E','F','G','H','I','J']
	#history=""
	def __init__(self,parent,board,move):
		self.board=board
		self.parent = parent
		self.depth = parent.depth + 1 if parent != None else 0
		self.move=move
		self.H1 = np.count_nonzero(self.board)
		self.F = self.depth + self.H1

	def getchildrens(self):
		locallist=[]
		for i in range(board.shape[0]):
			for j in range(board.shape[1]):
				locallist.append(flip(self,i,j))
		return locallist

	def printboard(self):
		print("GOAL\n",goal)
		print(self.board)

	# def printchildrens(self):
	# 	for index,i in enumerate(locallist):
	# 		print("children ",index+1,"\n",i.board)

	#def populateOpenlist(locallist):

# Get
def bubblesort(locallist):
	n=len(locallist)
	for i in range(n):
		for j in range(0, n-i-1):
			if locallist[j].F < locallist[j+1].F :
				locallist[j], locallist[j+1] = locallist[j+1], locallist[j]
			elif(locallist[j].F == locallist[j+1].F):
				pass
	return locallist

def flip(parentboard,row,column):
	localboard = np.array(parentboard.board)
	boardsize = localboard.shape[0]

	localcol,localrow = column,row
	indexes = []
	indexes.append((localrow,localcol))
	"""
	"""
	N,S,W,E = (localrow-1,localcol),(localrow+1,localcol),(localrow,localcol-1),(localrow,localcol+1)
	indexes.append(N)
	indexes.append(S)
	indexes.append(W)
	indexes.append(E)
	"""
	"""
	for i in indexes:
		if (i[0] < 0 or i[0] >= boardsize) or (i[1] < 0 or i[1] >= boardsize):
			continue
		else:
			if localboard[i[0],i[1]]==1:
				localboard[i[0],i[1]]=0
			else:
				localboard[i[0],i[1]]=1
	return Gameboard(parentboard,localboard,(row,column))

def findbestchild(boardlist):
	#number of total coin
	total = len(boardlist[0].board.flatten())
	bestchild = []
	temp=[]
	index = total
	#find all 0's position of a board, and put in turple in bestchild list
	#print("boardlist",boardlist)
	for board in boardlist:
		bestchild.append(([i for i, n in enumerate(board.board.flatten()) if n == 0],board))
	smallest = total
	if len(bestchild) == 1:
		return bestchild[0][1]
	#search bestchild for the smallest index number
	#print("Best children",bestchild)
	for i in bestchild:
		try:
			if i[0][0] < smallest:
				smallest=i[0][0]
				temp=[i]
			elif i[0][0]==smallest:
				temp.append(i)
		except:
			pass
	#print("Before While loop",temp)
	while(len(temp)>1):
		#print(temp)
		smallest = total
		bestchild=[]
		for i in temp:
			i[0].pop(0)
			bestchild.append((i[0],i[1]))
		for i in bestchild:
			try:
				if i[0][0] < smallest:
					smallest=i[0][0]
					temp=[i]
				elif i[0][0]==smallest and i[0][0]!=total:
					temp.append(i)
			except:
				pass
	print("Finally,", temp)	
	return temp[0][1]

def DFS(board,openlist,closelist,maxd):
	exist=False
	if np.array_equal(board.board,goal) or board.depth>maxd:
		return board
	if board.depth<maxd:
		closelist.append(board)
		childrens=board.getchildrens()
		sortedchildrens=[]
		total = len(childrens)
		print(total)
		for i in range(total):
			tempbestchild = findbestchild(childrens)
			sortedchildrens.append(tempbestchild)
			childrens.pop(childrens.index(tempbestchild))
		for i in reversed(sortedchildrens):
			for j in closelist:
				if np.array_equal(i.board,j.board):
					exist=True
			for j in openlist:
				if np.array_equal(i.board,j.board):
					exist=True
			if not exist:
				openlist.append(i)
		if len(openlist)==0:
			return board
		return DFS(openlist.pop(),openlist,closelist,maxd)

def BFS(board,openlist,closelist,maxl):
	exist = False
	potential =np.array([[0,0,0,0,1,0,1,1,1]]).reshape(3,3)
	#print(potential)
	if np.array_equal(board.board,goal) or board.depth>maxd:
		return board
	if board.depth<maxd:
		closelist.append(board)
		for i in reversed(bubblesort(board.getchildrens())):
			for j in closelist:
				if np.array_equal(i.board,j.board):
					exist=True
			for j in openlist:
				if np.array_equal(i.board,j.board):
					exist=True
			if not exist:
				openlist.append(i)
		if len(openlist)==0:
			return board
		nextboard = openlist.pop()
		# Gameboard.history+=str(Gameboard.alphabet[nextboard.move[0]])+str(nextboard.move[1])+" "
		# for i in nextboard.board.flatten():
		# 	Gameboard.history+=str(i)
		# Gameboard.history+="\n"
		return DFS(nextboard,openlist,closelist,maxd)
	else:
		return board


# def traceback(board,mystring):
# 	print(board.parent)
# 	if board.parent == None:
# 		print(board.board)
# 		return mystring
# 	else:
# 		mystring+="\n" + alphabet[board.move[0]]+str(board.move[1])+" "
# 		for i in board.board.flatten():
# 			mystring+=str(i)
# 		return traceback(board.parent,mystring)
	

if __name__ == '__main__':
	size = 0
	maxd = 0
	maxl = 0
	openlist=[]
	closelist=[]

	with open("input.txt","r") as file:
		inputstringlist = file.readline().split()
	size = int(inputstringlist[0])
	goal = np.zeros(size*size).reshape(size,size)
	maxd = int(inputstringlist[1])
	maxl = inputstringlist[2]
	board = list(inputstringlist[3].replace("\n",""))
	board = [int(i) for i in board]
	board = np.reshape(board,(size,size))
	initialboard = Gameboard(None,board,None)
	solutionboard = DFS(initialboard,openlist,closelist,maxd)
	print(solutionboard.board)
	print(len(closelist))
	for i in closelist:
		print(i.board)
	# print("best child-> ",findbestchild(initialboard.getchildrens()).board)
	# for i in initialboard.getchildrens():
	# 	print(i.board)
