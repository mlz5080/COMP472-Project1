import numpy as np
import math
import heapq
import _thread
import time
from operator import itemgetter

class Gameboard():
	alphabet=['A','B','C','D','E','F','G','H','I','J']
	#history=""
	def __init__(self,parent,board,move):
		self.board=board
		self.parent = parent
		self.depth = parent.depth + 1 if parent != None else 0
		self.move=move
		self.G = 0
		self.H = 0
		self.F = 0
		self.string = ''.join(str(x) for x in self.board.flatten())

	def UpdateHFG(self,matrix):
		self.G = self.depth
		self.H = np.count_nonzero(Solution(self,matrix))
		self.F += self.G+self.H

	def getchildrens(self):
		locallist=[]
		for i in range(board.shape[0]):
			for j in range(board.shape[1]):
				locallist.append(flip(self,i,j))
		return locallist

	def printboard(self):
		print("GOAL\n",goal)
		print(self.board)

	def __lt__(self, other):
		if self.F != other.F:
			return self.F<other.F
		else:
			result = rankbestchild([self,other])
			if result[0]==self:
				return True
			else:
				return False

# BubbleSort for sorting open list with their value of H.
def BubbleSort_F(locallist):
	n=len(locallist)
	for i in range(n):
		for j in range(0, n-i-1):
			if locallist[j].F < locallist[j+1].F :
				locallist[j], locallist[j+1] = locallist[j+1], locallist[j]
			elif(locallist[j].F == locallist[j+1].F):
				pass
	return locallist

# BubbleSort for sorting open list with their value of H.
def BubbleSort_H(locallist):
	n=len(locallist)
	for i in range(n):
		for j in range(0, n-i-1):
			if locallist[j].H < locallist[j+1].H :
				locallist[j], locallist[j+1] = locallist[j+1], locallist[j]
			elif(locallist[j].H == locallist[j+1].H):
				pass
	return locallist

#Flip function that can flip each position and their adjacent nodes
def flip(parentboard,row,column):
	localboard = np.array(parentboard.board)
	boardsize = localboard.shape[0]
	localcol,localrow = column,row
	indexes = []
	indexes.append((localrow,localcol))
	N,S,W,E = (localrow-1,localcol),(localrow+1,localcol),(localrow,localcol-1),(localrow,localcol+1)
	indexes.append(N)
	indexes.append(S)
	indexes.append(W)
	indexes.append(E)
	for i in indexes:
		if (i[0] < 0 or i[0] >= boardsize) or (i[1] < 0 or i[1] >= boardsize):
			continue
		else:
			if localboard[i[0],i[1]]==1:
				localboard[i[0],i[1]]=0
			else:
				localboard[i[0],i[1]]=1
	return Gameboard(parentboard,localboard,(row,column))

def rankbestchild(boardlist):
	temp=[(i.string,i) for i in boardlist]
	temp.sort(key=itemgetter(0))
	return [i[1] for i in temp[::-1]]

def BubbleSort_string(mylist):
	n = len(mylist)
	for i in range(n):
		for j in range(0, n-i-1):
			if mylist[j].string < mylist[j+1].string:
				mylist[j], mylist[j+1] = mylist[j+1], mylist[j]
	return mylist

def DFS(board,openlist,closelist,maxd):
	localboard=board
	closelistsets=set()
	openlistsets=set()
	while True:
		if np.array_equal(localboard.board,goal) :
			return localboard
		elif localboard.depth==maxd:
			closelist.append(localboard)
			closelistsets.add(localboard.string)
			localboard=openlist.pop()
		else:
			closelist.append(localboard)
			closelistsets.add(localboard.string)
			childrens=localboard.getchildrens()
			childrens = rankbestchild(childrens)
			for i in childrens:
				if i.string not in closelistsets or i.string not in openlistsets:
					openlistsets.add(i.string)
					openlist.append(i)
			if len(openlist)==0:
				return localboard
			localboard=openlist.pop()

#These functions gives you exact steps to solve the puzzle if
#it has a solution
def determine_one_zero(i,j,shape):
	if i==j:
		return 1
	elif (math.ceil(j/shape)==math.ceil(i/shape)) and (j+1 ==i or j-1==i):
		return 1
	elif j%shape == i%shape and (j-shape == i or j+shape==i):
		return 1
	else:
		return 0

#Heuristic function
def Solution(board,lhsmatrix):
	rhsvector = board.board.flatten()
	newshape = board.board.shape[0]
	temp = np.floor(np.linalg.solve(lhsmatrix, rhsvector)%2)
	return temp.reshape(newshape,newshape)

def BFS(board,openlist,closelist,maxl):
	exist=False
	localboard=board
	size = len(board.board.flatten())
	lhsmatrix=[]
	for i in range(1,size+1):
		for j in range(1,size+1):
			lhsmatrix.append(determine_one_zero(i,j,board.board.shape[0]))
	lhsmatrix = np.array(lhsmatrix).reshape(size,size)
	closelistsets = set()
	openlistsets = set()

	while True:
		if np.array_equal(localboard.board,goal) or len(closelist)==maxl :
			return localboard
		closelist.append(localboard)
		closelistsets.add(localboard.string)
		childrens=localboard.getchildrens()

		for i in childrens:
			i.UpdateHFG(lhsmatrix)
			if i.string not in closelistsets or i.string not in openlistsets:
				heapq.heappush(openlist, (i.H, i))
				openlistsets.add(i.string)
		if len(openlist)==0:
			return localboard
		localboard=heapq.heappop(openlist)[1]

def Astar(board,openlist,closelist,maxl):
	#initialization
	localboard=board
	closelistsets=set()
	openlistsets=set()
	size = len(board.board.flatten())
	lhsmatrix=[]
	for i in range(1,size+1):
		for j in range(1,size+1):
			lhsmatrix.append(determine_one_zero(i,j,board.board.shape[0]))
	lhsmatrix = np.array(lhsmatrix).reshape(size,size)

	while True:
		if np.array_equal(localboard.board,goal) or len(closelist)==maxl :
			return localboard

		closelist.append(localboard)
		closelistsets.add(localboard.string)
		childrens=localboard.getchildrens()
		for i in childrens:
			i.UpdateHFG(lhsmatrix)
			if i.string not in closelistsets or i.string not in openlistsets:
				heapq.heappush(openlist, i)
				openlistsets.add(i.string)
		if len(openlist)==0:
			return localboard
		localboard=heapq.heappop(openlist)

def traceback(board):
	if board.parent == None:
		mystring = "0 "
		for i in board.board.flatten():
			mystring+=str(i)
		mystring+="\n"
		return mystring
	else:
		parentstring = traceback(board.parent)
		parentstring+=Gameboard.alphabet[board.move[0]]+str(board.move[1])+" "
		for i in board.board.flatten():
			parentstring+=str(i)
		parentstring+="\n"
		return parentstring

def searchfile(closelist):
	mystring = ""
	for i in closelist:
		mystring+= str(i.F) + " " + str(i.G) + " " + str(i.H) +" "
		for j in i.board.flatten():
			mystring+=str(j)
		mystring+="\n"
	return mystring

def DFS_wrapper(initialboard,openlist,closelist,maxd,index):
	solutionboard = DFS(initialboard,openlist,closelist,maxd)
	with open(str(index)+"_dfs_search.txt","w") as file:
		file.write(searchfile(closelist))
	with open(str(index)+"_dfs_solution.txt","w") as file:
		if not np.array_equal(solutionboard.board,goal):
			file.write("No solution!")
		else:
			file.write(traceback(solutionboard))

def BFS_wrapper(initialboard,openlist,closelist,maxl,index):
	solutionboard = BFS(initialboard,openlist,closelist,maxl)
	with open(str(index)+"_bfs_search.txt","w") as file:
		file.write(searchfile(closelist))
	with open(str(index)+"_bfs_solution.txt","w") as file:
		if not np.array_equal(solutionboard.board,goal):
			file.write("No solution!")
		else:
			file.write(traceback(solutionboard))

def Astar_wrapper(initialboard,openlist,closelist,maxl,index):
	solutionboard = Astar(initialboard,openlist,closelist,maxl)
	with open(str(index)+"_astar_search.txt","w") as file:
		file.write(searchfile(closelist))
	with open(str(index)+"_astar_solution.txt","w") as file:
		if not np.array_equal(solutionboard.board,goal):
			file.write("No solution!")
		else:
			file.write(traceback(solutionboard))

if __name__ == '__main__':
	size = 0
	maxd = 0
	maxl = 0
	openlist=[]
	closelist=[]

	with open("input.txt","r") as file:
		for index,line in enumerate(file):
			inputstringlist = line.split()
			size = int(inputstringlist[0])
			goal = np.zeros(size*size).reshape(size,size)
			maxd = int(inputstringlist[1])
			maxl = int(inputstringlist[2])
			board = list(inputstringlist[3].replace("\n",""))
			board = [int(i) for i in board]
			board = np.reshape(board,(size,size))
			initialboard = Gameboard(None,board,None)
			#print(Solution(initialboard))
			DFS_wrapper(initialboard,[],[],maxd,index)
			BFS_wrapper(initialboard,[],[],maxl,index)
			Astar_wrapper(initialboard,[],[],maxl,index)