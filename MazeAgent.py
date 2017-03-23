import Queue as Q
from math import *
import datetime

class MazeAgent(object):
    '''
    Agent that uses path planning algorithm to figure out path to take to reach goal
    Built for Malmo discrete environment and to use Malmo discrete movements
    '''

    def __init__(self, grid=None):
        self.__frontier_set = None
        self.__explored_set = None
        self.__goal_state = None
        self.__grid = grid
        self.start = None # type tuple


    def get_eset(self):
        return self.__explored_set

    def get_fset(self):
        return self.__frontier_set

    def get_goal(self):
        return self.__goal_state

    def set_grid(self, grid):
        self.__grid = grid

    def set_start(self, start, tup):
        self.start = tup

    def set_all_none(self):
        self.__frontier_set = None
        self.__explored_set = None
        self.__goal_state = None
        self.start = None # type tuple

    def __plan_path_breadth(self):
        '''Breadth-First tree search'''

        # Make frontier set a queue and add the starting tile
        self.__frontier_set = Q.Queue()
        self.start = self.find_val(2)
        self.__frontier_set.put(self.start)

        # Make explored set a dictionary and add the starting tile's coordinates
        # Key = the coordinates of a tile, value = the previous tile we came from
        self.__explored_set = {(self.start[0], self.start[1]) : None}

        # While the frontier set isn't empty
        while not self.__frontier_set.empty():
            # Pop off an item
            curr = self.__frontier_set.get()
            # If this is the goal tile, return the path
            if self.__grid[curr[0]][curr[1]] == 3:
                return 
            # Otherwise, get the possible neighbors we can move to from this tile and add them to frontier set
            else:
                neighbors = self.get_neighbors(curr[0], curr[1])
                for n in neighbors:
                    self.__frontier_set.put(n)


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



    def __plan_path_astar(self):
        '''A* tree search'''

        # Make frontier set a priority queue
        self.__frontier_set = Q.PriorityQueue()

        # Find start and goal states
        self.start = self.find_val(2)
        self.__goal_state = self.find_val(3)

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

    def get_distance(self, prev, curr):
        ''' gets manhattan distance between two nodes'''
        return abs(prev[0] - curr[0]) + abs(prev[1] - curr[1])

    def get_path(self):
        '''should return list of strings where each string gives movement command
            (these should be in order)
            Example:
             ["movenorth 1", "movesouth 1", "moveeast 1", "movewest 1"]
             (these are also the only four commands that can be used, you
             cannot move diagonally)
             On a 2D grid (list), "move north" would move us
             from, say, [0][0] to [1][0]
        '''

        t1 = datetime.datetime.now()
        self.__plan_path_breadth()
        #self.__plan_path_astar()
        t2 = datetime.datetime.now()

        print("Time to find path: " + str(t2-t1)[5:])
        
        
        output = []
        curr = self.find_val(3)
        prev = self.__explored_set[curr]

        # While the value for a key is not None
        # Starting with our goal state, we look through the dictionary and trace back the path using the keys/values
        num_instr = 0
        while prev != None:
            output = [self.which_direction(prev, curr)] + output
            curr = prev
            prev = self.__explored_set[curr]
            num_instr += 1

        print("Total number of instruction: " + str(num_instr))

        self.set_all_none()
        
        return output


    def which_direction(self, prev, curr):
        ''' returns the movement command'''
        if prev[0] < curr[0]:
            return "movenorth 1"
        if prev[0] > curr[0]:
            return "movesouth 1"
        if prev[1] < curr[1]:
            return "movewest 1"
        if prev[1] > curr[1]:
            return "moveeast 1"

    def find_val(self,val):
        '''returns the location of a value in the grid'''
        return [(index, row.index(val)) for index, row in enumerate(self.__grid) if val in row][0] # http://stackoverflow.com/questions/17385419/find-indices-of-a-value-in-2d-matrix
