#Project 2015 1XA3
#by: Cesar Antonio Santana Penner

from random import *
from graphics import *

'''
This is a program that generates a perfect (N*N) maze using a Depth-First Search Alogrithm.
This program can also solve itself. The green square represents the start of the maze 
, the blue square represents the key and the red sqaure represents the end. The solution 
path from the start to the key is highlighted with a path of yellow squares and the path
from the key to the end is highlighted with orange squares. 
'''
#stack (LIFO)
class MyStack:
	def __init__(self):
		pass 
	def push(item,S):
		return [item] + S
	def pop(S):
		return S.pop(0) 
	def isEmpty(S):
		return True if len(S)==0 else False
	def size(S):
		return len(S)

#class Maze that can generate a perfect maze, draw itself, and solve itself
class Maze:
	def __init__(self,N):
		mazeList = []
		mazeXY = []
		for i in range(N+2):
			mazeList.append(["*"]*(N+2))
			mazeXY.append(["*"]*(N+2))
		for i in range(N+2):
			for j in range(N+2):
				mazeXY[i][j] = [i,j]
				mazeList[i][j] = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[1,1,1,1]] 
		self.Maze = mazeList
		self.Size = N + 2
		self.XY = mazeXY
		self.first = [0,0]
		self.end = [0,0]
		kx,ky = randint(1,self.Size-2),randint(1,self.Size-2)
		self.key = [kx,ky]
		Rx2,Ry2 = randint(1,self.Size-2),randint(1,self.Size-2)
		self.end = [Rx2,Ry2]
		while self.end == self.first:
			if Rx2 == self.first[0] and Ry2 ==self.first[1]: 
				Rx2,Ry2 = randint(1,self.Size-2),randint(1,self.Size-2)
			self.end = [Rx2,Ry2]
		while (kx == Rx2 or kx == self.first[0]) and (ky == Ry2 or ky == self.first[1]):
			kx,ky = randint(1,self.Size-2),randint(1,self.Size-2)
			self.key = [kx,ky]

		self.SolutionPath = []
		self.keyPath = []		
		
	def border(self): # sets border of maze
		for j in range(self.Size):
			for i in range(self.Size):
				#northern border
				if j == 0:
					self.Maze[j][i][2][0] = 1#"North"
				#south border
				elif j == self.Size-1:
					self.Maze[j][i][2][3] = 1#"South"
				#western border
				elif i == 0:
					self.Maze[j][i][2][2] = 1#"West"
				#east border
				elif i == self.Size-1:
					self.Maze[j][i][2][1] =1#"East"

	def genMaze(self): #generates Maze
		CellStack = []
		TotalCells = (self.Size-2) * (self.Size -2)
		x,y= randint(1,self.Size-2),randint(1,self.Size-2)
		CurrentCell = [x,y]
		VisitedCells = 1
		self.first = [x,y]

		while VisitedCells < TotalCells:
			walls = [0,0,0,0]
			#checks if current cells' neighbors have all their walls up, which determines which direction the next cell can be 
			if sum(self.Maze[x][y-1][3]) == 4 and sum(self.Maze[x][y-1][2]) == 0: # north
				walls[0] = 1
			if sum(self.Maze[x+1][y][3]) == 4 and sum(self.Maze[x+1][y][2]) == 0: #east 
				walls[1] = 1 
			if sum(self.Maze[x-1][y][3]) == 4 and sum(self.Maze[x-1][y][2]) == 0: #west
				walls[3] = 1
			if sum(self.Maze[x][y+1][3]) ==4 and sum(self.Maze[x][y+1][2])==0: #south
				walls[2] = 1


			if sum(walls) >=1:#as long as current cell has at least one neighbor with all their walls up
				side = chooseSide(walls)
				CurrentCell = [x,y]
				CellStack = MyStack.push(CurrentCell,CellStack)
				if side == "done":
					pass
				elif side == "Up":
					self.Maze[x][y][3][0] = 0
					self.Maze[x][y-1][3][2] = 0
					x = x
					y = y-1
				elif side == "Right":
					self.Maze[x][y][3][1] = 0
					self.Maze[x+1][y][3][3] = 0
					x = x+1
					y =y 
				elif side == "Left":
					self.Maze[x][y][3][3] = 0
					self.Maze[x-1][y][3][1] = 0
					x = x-1
					y=y
				elif side == "Down":
					self.Maze[x][y][3][2] = 0
					self.Maze[x][y+1][3][0] = 0
					x = x
					y = y+1
				VisitedCells +=1

			else:
				CurrentCell = MyStack.pop(CellStack)
				x = CurrentCell[0]
				y = CurrentCell[1]
	
	def Draw(self):#draws maze
		win = GraphWin("Maze",20*self.Size,20*self.Size)
		myrect = Rectangle(Point(0,0),Point(20,20))
		myrect.draw(win)
		#draws grid
		for i in range(1,self.Size-1):
			for j in range(1,self.Size-1):
				myrect = Rectangle(Point(0+20*i,0+20*j),Point(20+20*i,20+20*j))
				myrect.setOutline('black')
				myrect.draw(win)
		#draw white lines over the walls that have been broken down
		for i in range(0,self.Size):
			for j in range(0,self.Size):
				if sum(self.Maze[i][j][2]) >=2:
					myrect = Rectangle(Point(0+20*i,0+20*j),Point(20+20*i,20+20*j))
					myrect.setOutline('white')
					myrect.draw(win)
				else:
					if self.Maze[i][j][3][0]==0:
						myline = Line(Point(1+20*i,0+20*j),Point(19+20*i,0+20*j))
						myline.setOutline("white")
						myline.draw(win)
					if self.Maze[i][j][3][1]==0:
						myline = Line(Point(20+20*i,1+20*j),Point(20+20*i,19+20*j))
						myline.setOutline("white")
						myline.draw(win)
					if self.Maze[i][j][3][2]==0:
						myline = Line(Point(1+20*i,20+20*j),Point(19+20*i,20+20*j))
						myline.setOutline("white")
						myline.draw(win)
					if self.Maze[i][j][3][3]==0:
						myline = Line(Point(0+20*i,1+20*j),Point(0+20*i,19+20*j))
						myline.setOutline("white")
						myline.draw(win)
		
		#draw path from start to key
		for cell in self.keyPath:
					myrect = Rectangle(Point(5+20*cell[0],5+20*cell[1]),Point(15+20*cell[0],15+20*cell[1]))
					myrect.setFill("Yellow")
					myrect.draw(win)
		#draw path from kay to end
		for cell in self.SolutionPath:
					myrect = Rectangle(Point(5+20*cell[0],5+20*cell[1]),Point(15+20*cell[0],15+20*cell[1]))
					myrect.setFill("tan1")
					myrect.draw(win)

		#draw start,key, and end rectangles
		start = Rectangle(Point(2+20*self.first[0],2+20*self.first[1]),Point(18+20*self.first[0],18+20*self.first[1]))
		start.setFill("green")
		start.draw(win)
		end = Rectangle(Point(2+20*self.end[0],2+20*self.end[1]),Point(18+20*self.end[0],18+20*self.end[1]))
		end.setFill("red")
		end.draw(win)
		key = Rectangle(Point(2+20*self.key[0],2+20*self.key[1]),Point(18+20*self.key[0],18+20*self.key[1]))
		key.setFill("blue")
		key.draw(win)
		
		win.mainloop()
	
	def Explore(self):#solves the maze
		#from start to key
		x,y= self.first[0],self.first[1]
		VisitedCells = 0
		TotalCells = (self.Size-2)**2
		CurrentCell = [x,y]
		CellStack = []
		
		while VisitedCells < TotalCells:
			if CurrentCell[0] == self.key[0] and CurrentCell[1] ==self.key[1]: 
				VisitedCells = TotalCells
				self.keyPath = MyStack.push(CurrentCell,CellStack)
				print("Path from the start to the key")
				print(self.keyPath)
			else:
				#walls that you can explore/go through
				walls = [0,0,0,0]
				if self.Maze[x][y][3][0]== 0 and self.Maze[x][y][1][0]==0: # north
					walls[0] = 1
				if self.Maze[x][y][3][1]==0 and self.Maze[x][y][1][1]==0: #east 
					walls[1] = 1 
				if self.Maze[x][y][3][3]==0 and self.Maze[x][y][1][3]==0: #west
					walls[3] = 1
				if self.Maze[x][y][3][2] ==0 and self.Maze[x][y][1][2]==0: #south
					walls[2] = 1

				if sum(walls) >=1:
					side = chooseSide(walls)
					CurrentCell = [x,y]
					CellStack = MyStack.push(CurrentCell,CellStack)
					if side == "done":
						pass
					elif side == "Up":
						self.Maze[x][y][1][0] = 1
						x = x
						y = y-1
						self.Maze[x][y][1][2] = 1
					elif side == "Right":
						self.Maze[x][y][1][1] = 1
						x = x+1
						y =y 
						self.Maze[x][y][1][3] = 1
					elif side == "Left":
						self.Maze[x][y][1][3] = 1
						x = x-1
						y=y
						self.Maze[x][y][1][1] = 1
					elif side == "Down":
						self.Maze[x][y][1][2] = 1
						x = x
						y = y+1
						self.Maze[x][y][1][0] = 1
					CurrentCell = [x,y]
				else:
					CurrentCell = MyStack.pop(CellStack)
					x = CurrentCell[0]
					y = CurrentCell[1]


		#form key to end
		#reset variables
		x,y= self.key[0],self.key[1]
		VisitedCells = 0
		TotalCells = (self.Size-2)**2
		CurrentCell = [x,y]
		CellStack = []

		#reset backtrack
		for i in range(self.Size):
			for j in range(self.Size):
				self.Maze[i][j][1] = [0,0,0,0]


		while VisitedCells < TotalCells:
			if CurrentCell[0] == self.end[0] and CurrentCell[1] ==self.end[1]: 
				VisitedCells = TotalCells
				self.SolutionPath = MyStack.push(CurrentCell,CellStack)
				print("Path from the key to the end")
				print(self.SolutionPath)
			else:
				#walls that you can explore/go through
				walls = [0,0,0,0]
				if self.Maze[x][y][3][0]== 0 and self.Maze[x][y][1][0]==0: # north
					walls[0] = 1
				if self.Maze[x][y][3][1]==0 and self.Maze[x][y][1][1]==0: #east 
					walls[1] = 1 
				if self.Maze[x][y][3][3]==0 and self.Maze[x][y][1][3]==0: #west
					walls[3] = 1
				if self.Maze[x][y][3][2] ==0 and self.Maze[x][y][1][2]==0: #south
					walls[2] = 1

				if sum(walls) >=1:
					side = chooseSide(walls)
					CurrentCell = [x,y]
					CellStack = MyStack.push(CurrentCell,CellStack)
					if side == "done":
						pass
					elif side == "Up":
						self.Maze[x][y][1][0] = 1
						x = x
						y = y-1
						self.Maze[x][y][1][2] = 1
					elif side == "Right":
						self.Maze[x][y][1][1] = 1
						x = x+1
						y =y 
						self.Maze[x][y][1][3] = 1
					elif side == "Left":
						self.Maze[x][y][1][3] = 1
						x = x-1
						y=y
						self.Maze[x][y][1][1] = 1
					elif side == "Down":
						self.Maze[x][y][1][2] = 1
						x = x
						y = y+1
						self.Maze[x][y][1][0] = 1
					CurrentCell = [x,y]
				else:
					CurrentCell = MyStack.pop(CellStack)
					x = CurrentCell[0]
					y = CurrentCell[1]


#funciton that determines what direction to ge next randomly
def chooseSide(myList):
	mybool = True 
	if sum(myList) == 0:#if their are no neighbors with all their walls up, you know you are done
		return "done"
	else:
		while mybool == True:
			side = randint(1,4)
			if side ==1 and myList[0]==1:
				return "Up"
			elif side ==2 and myList[1]==1:
				return "Right"
			elif side ==3 and myList[2]==1:
				return "Down"
			elif side ==4 and myList[3]==1: 
				return "Left"


def main():
	a = Maze(30)
	a.border()
	a.genMaze()
	a.Explore()
	a.Draw()
main()
