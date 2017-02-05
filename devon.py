
import generals
import heapq


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
				print("updated tile: "+str(i)+" "+str(j))

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
		pass



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


	def createMap(self, update):
		'''Craetes the initial Map - a 2D array with a
		Tile object in each index'''
		#print("creating map!")
		self.nCols = update['cols']
		self.nRows = update['rows']
		self.mapGrid = [ [Tile() for i in range(self.nCols)] for j in range(self.nRows) ]



	def printMap(self, update):
		print("")
		for i in range(len(update['tile_grid'])):
			rowStr = ""
			for j in range(len(update['tile_grid'][i])):
				tile =  update['tile_grid'][i][j]
				if tile == generals.MOUNTAIN:
					rowStr += "[ M ]"
				elif tile == generals.FOG:
					rowStr += "[   ]"
				elif tile == generals.OBSTACLE:
					rowStr += "[ M ]"
				elif tile == 0:
					rowStr += "[ O ]"
				elif tile == 1:
					rowStr += "[ X ]"
				elif tile == -1:
					rowStr += "[ s ]"
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

for update in frank.game.get_updates():
#	frank.printMap(update)
	if madeMap == False:
		frank.initializeMap(update)
		madeMap = True
		pi = update['player_index']
		crownY, crownX = update['generals'][pi]
		print("Crown is at [x,y]: [" + str(crownX) + "," + str(crownY) + "]")
	
	print("Crown: " + str(update['tile_grid'][crownY][crownX]))
	print("Up: " + str(update['tile_grid'][crownY - 1][crownX]))
	print("Down: " + str(update['tile_grid'][crownY + 1][crownX]))
	print("Left: " + str(update['tile_grid'][crownY][crownX - 1]))
	print("Right: " + str(update['tile_grid'][crownY][crownX + 1]))

	

	y, x = update['generals'][pi]
	print("x: " + str(x))
	print("y: " + str(y))
	# move units from general to arbitrary square

	for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
		if (0 <= y+dy < update['rows'] and 0 <= x+dx < update['cols'] and update['tile_grid'][y+dy][x+dx] == 0):
			frank.game.move(y, x, y+dy, x+dx)
			break
