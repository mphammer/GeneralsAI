import generals
import heapq


import Queue as Q
from math import *
import datetime


# 1v1
#g = generals.Generals('ry0FVyx_g', 'frank', '1v1')

# ffa
# g = generals.Generals('your userid', 'your username', 'ffa')

# private game
#roomID = raw_input("Please enter the room id: ")
#print(roomID)

#g = generals.Generals('ry0FVyx_g', 'frank', 'private', roomID)

# 2v2 game
# g = generals.Generals('your userid', 'your username', 'team')

RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)


class Tile:
	def __init__(self):
		self.state = generals.FOG  # what is on the tile
		self.visited = False       # while traversing, marks if visited
		self.coords = []           # coordinates in grid
		self.up = None             # Node above it
		self.down = None           # Node below it
		self.left = None           # Node to left of it
		self.right = None          # Node to right of it
		self.army = 0              # Number of troops on the tile (- means good)
		self.searchDist = 0        #
		self.searchPrev = None



class Bot:
	def __init__(self):
		self.mapGrid = []      # a representation of the map as a 2x2 matrix
		self.tiles = []   	   # a list of all tiles
		self.roomID = ""       # the id of current game
		self.nCols = 0         # number of columns in the map
		self.nRows = 0         # number of rows in the map
		self.game = None
		self.color = ""

	def startGame(self,game="private"):
		if game == "1v1":
			self.game = generals.Generals('ry0FVyx_g', 'frank', '1v1')
		elif game == "ffa":
			self.game = generals.Generals('ry0FVyx_g', 'frank', 'ffa')
		elif game == "private":
			self.roomID = raw_input("Please enter the room id: ")
			self.game = generals.Generals('ry0FVyx_g', 'frank', 'private', self.roomID)
		elif game == "2v2":
			self.game = generals.Generals('ry0FVyx_g', 'frank', 'team')
		else:
			print("Please input one of the following game types: ")
			print("1v1, ffa, private, 2v2")


	def initializeMap(self,update):
		'''Creates a map with nodes and connects the nodes
		to create a graph that the bot can traverse'''

		self.createMap(update)

		for i in range(self.nRows):
			for j in range(self.nCols):
				#print("updated tile: "+str(i)+" "+str(j))

				currTile = self.mapGrid[i][j]
				currTile.coords = [i,j]

				if i+1 < self.nRows:                                         # check down
					if update['tile_grid'][i+1][j] in [generals.FOG,1,-1]:
						currTile.down = self.mapGrid[i+1][j]

				if i-1 >= 0:                                                 # check up
					if update['tile_grid'][i-1][j] in [generals.FOG,1,-1]:
						currTile.up = self.mapGrid[i-1][j]

				if j+1 < self.nCols:                                         # check right
					if update['tile_grid'][i][j+1] in [generals.FOG,1,-1]:
						currTile.right = self.mapGrid[i][j+1]

				if j-1 >= 0:                                                 # check left
					if update['tile_grid'][i][j-1] in [generals.FOG,1,-1]:
						currTile.left = self.mapGrid[i][j-1]


	def updateMap(self,update):
		for i in range(self.nRows):
			for j in range(self.nCols):
				botTile = self.mapGrid[i][j]
				tile =  update['tile_grid'][i][j]
				troops = update['army_grid'][i][j]
				if tile == generals.MOUNTAIN:
					botTile.state = generals.MOUNTAIN
				elif tile == generals.FOG:
					botTile.state = generals.FOG
				elif tile == generals.OBSTACLE:
					botTile.state = generals.OBSTACLE
				elif tile == generals.ENEMY:
					botTile.state = generals.ENEMY
					botTile.army = troops
					if self.color == "blue":
						botTile.army *= -1
				elif tile == generals.BOT:
					botTile.state = generals.BOT
					botTile.army = troops
					if self.color == "red":
						botTile.army *= -1
				elif tile == generals.EMPTY:
					botTile.state = generals.EMPTY
				else:
					print("unknown state")



	def dijkstras(self,root,target):
		heap = []
		for t in self.tiles:
			t.searchDist = 1000000
			t.searchPrev = None
			root.searchDist = 0
			heapp.heappush(heap,t)
		while heap != []:
			u = heapq.heappop(heap)
			for v in [u.up,u.down,u.left,u.right]:
				if v:
					alt = u.searchDist + v.army
					if alt < v.searchDist:
						v.searchDist = alt
						v.searchPrev = u
		return target


	def A_star(self,target):
                '''A* tree search'''

                # Make frontier set a priority queue
                self.__frontier_set = Q.PriorityQueue()

                # Find start and goal states
                self.start = self.find_val(2)
                self.__goal_state = target

                # Add the start tile to the frontier set, using the distance between it and the goal state as it's priority
                # This is calculated in our get_distance() fucntion using Manhattan distance
                self.__frontier_set.put(self.start, self.get_distance(self.start, self.__goal_state))

                # create dictionary to track distances traveled so far
                cost_so_far = {}

                # Add start state to explored set, using same dictionary method as befor
                self.__explored_set = {(self.start[0], self.start[1]) : None}
                # Add start state to cost so far, 0 distance from itself
                cost_so_far = {(self.start[0], self.start[1]) : 0}

                # While there's something in the frontier set
                while not self.__frontier_set.empty():
                    # Pop off the item with highest priority/lowest distance to goal state (heuristic value)
                    curr = self.__frontier_set.get()
                    # If this is the goal state, return path
                    if self.__grid[curr[0]][curr[1]] == 3:
                        return 
                    # Otherwise, find the neighbors and add them to the frontier set with their distance to goal/priority
                    else:
                        neighbors = self.get_neighbors(curr[0], curr[1])
                        for n in neighbors:
                            # update the neightbors cost so far (1 more than previous position)
                            cost_so_far[n] = cost_so_far[curr] + 1
                            # find new heuristic for a neighbor
                            new_heuristic = cost_so_far[n] + self.get_distance(n, self.__goal_state)
                            # add the heuristic for the neighbor to the fontier set
                            self.__frontier_set.put(n, self.get_distance(n, curr))
                return "No Path Found"
        

        def get_neighbors(self,r,c):
                ''' Returns a list of valid neighbors for a given node. Makes sure that the adjacent
                    rows/columns are valid indices and that we don't already have the tile in our explored set.
                    Adds valid neighbor tiles to the list of neighbors and also the explored set.'''

                # When adding neighbors to the explored set, notice how we are setting the key to be the neighbor tile
                # and the value as the tile we just came from. This will allow us to create the path in get_path() and
                # which_direction() later on.

                neighbors = []

                # row below
                if (r+1) < len(self.__grid):
                    row_below = self.__grid[r+1][c]
                    if (row_below in [1,3]) and (self.__explored_set.get((r+1,c)) == None):
                        neighbors += [(r+1,c)]
                        self.__explored_set[(r+1,c)] = (r,c)

                # row above
                if (r-1) >= 0:
                    row_above = self.__grid[r-1][c]
                    if (row_above in [1,3])and (self.__explored_set.get((r-1,c)) == None):
                        neighbors += [(r-1,c)]
                        self.__explored_set[(r-1,c)] = (r,c)

                # column to the right
                if (c+1) < len(self.__grid[0]):
                    right_col = self.__grid[r][c+1]
                    if (right_col in [1,3]) and (self.__explored_set.get((r,c+1)) == None) :
                        neighbors += [(r,c+1)]
                        self.__explored_set[(r,c+1)] = (r,c)

                # coulumn to the left
                if (c-1) >= 0:
                    left_col = self.__grid[r][c-1]
                    if (left_col in [1,3]) and (self.__explored_set.get((r,c-1)) == None):
                        neighbors += [(r,c-1)]
                        self.__explored_set[(r,c-1)] = (r,c)
                return neighbors


        def get_distance(self, prev, curr):
                ''' gets manhattan distance between two nodes'''
                return abs(prev[0] - curr[0]) + abs(prev[1] - curr[1])


        def find_val(self,val):
                '''returns the location of a value in the grid'''
                return [(index, row.index(val)) for index, row in enumerate(self.__grid) if val in row][0] # http://stackoverflow.com/questions/17385419/find-indices-of-a-value-in-2d-matrix


	def createMap(self, update):
		'''Craetes the initial Map - a 2D array with a 
		Tile object in each index'''
		self.nCols = update['cols']
		self.nRows = update['rows']
		self.mapGrid = [ [Tile() for i in range(self.nCols)] for j in range(self.nRows) ]



	def printMap(self):
		print("")
		for i in range(self.nRows):
			rowStr = ""
			for j in range(self.nCols):
				tile =  self.mapGrid[i][j]
				if tile.state == generals.MOUNTAIN:
					rowStr += "[ M ]"
				elif tile.state == generals.FOG:
					rowStr += "[|||]"
				elif tile.state == generals.OBSTACLE:
					rowStr += "[ M ]"
				elif tile.state == generals.ENEMY:
					rowStr += "[ "+str(tile.army)+" ]"
				elif tile.state == generals.BOT:
					rowStr += "[ "+str(tile.army)+" ]"
				elif tile.state == generals.EMPTY:
					rowStr += "[   ]"
				else:
					rowStr += "[ "+str(tile)+" ]"
			print(rowStr)
		print("")
		print("")



frank = Bot()
frank.startGame()

madeMap = False

stackX = 0
stackY = 0

curDir = None

for update in frank.game.get_updates():
	frank.printMap()
	if madeMap == False:
		frank.initializeMap(update)
		pi = update['player_index']
		crownY, crownX = update['generals'][pi]
		
		if frank.mapGrid[crownY][crownX].army > 0:
			frank.color = "red"
		else:
			frank.color = "blue"
		
		stackX = crownX
		stackY = crownY
		madeMap = True
		
	frank.updateMap(update)
	if frank.mapGrid[stackY][stackX].army > -1:
		stackX = crownX
		stackY = crownY

#	print("Stack: [" + str(stackX) + "," + str(stackY) + "]")

	attacked = False

	for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
		if frank.mapGrid[stackY+dy][stackX + dx].army  >= 1:
			frank.game.move(stackY, stackX, stackY + dy, stackX + dx)
			stackX += dx
			stackY += dy
			attacked = True
			break



	if attacked == False:
		if curDir != None:
                        print(curDir)
			dy, dx = curDir
			if frank.mapGrid[stackY+dy][stackX+dx].army <= -1:
				frank.game.move(stackY, stackX, stackY + dy, stackX + dx)
				stackX += dx
				stackY += dy
				
			else:
                                if curDir == UP or curDir == DOWN:
                                        dy, dx = LEFT
                                        if frank.mapGrid[stackY+dy][stackX+dx].army <= -1:
                                                print("HEADING LEFT")
                                                curDir = LEFT
                                        else:
                                                print("HEADING RIGHT")
                                                curDir = RIGHT
                                else:
                                        dy, dx = UP
                                        if frank.mapGrid[stackY+dy][stackX+dx].army <= -1:
                                                print("HEADING UP")
                                                curDir = UP
                                        else:
                                                print("HEADING DOWN")
                                                curDir = DOWN
                                dy, dx = curDir
                                frank.game.move(stackY, stackX, stackY + dy, stackX + dx)
				stackX += dx
				stackY += dy
				
				
		else:
                        print("flipping")
			for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:		
				if frank.mapGrid[stackY+dy][stackX+dx].army <= -1:
					frank.game.move(stackY, stackX, stackY + dy, stackX + dx)
					stackX += dx
					stackY += dy
					curDir = (dy, dx)
					break                        
