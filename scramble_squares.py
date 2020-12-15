# This program solves the scrambled squares puzzle where the puzzle pieces
# must be arranged in a 3 x 3 grid with the images on the edges lined up
# correctly (e.g. the top mating with the corresponding bottom).
# This puzzle is deceptively hard to solve as the tiles can be rotated as
# well as permuated. This means there are 4^9 * 9! combinations, although
# only around 10,000 are valid.

import json
import sys

class Tile:
    def __init__(self, param=None):
        if isinstance(param, Tile):
            self.copy_constructor(param)
        else:
            self.non_copy_constructor(param)

    def non_copy_constructor(self, json):
        self.name = json["name"]
        self.west = json["west"]
        self.north = json["north"]
        self.east = json["east"]
        self.south = json["south"]
        self.direction = 0

    def copy_constructor(self, orig):
        self.name = orig.name
        self.west = orig.west
        self.north = orig.north
        self.east = orig.east
        self.south = orig.south
        self.direction = orig.direction

    def __str__(self):
        retVal = ("Name=" + self.name + ", west=" + self.west +
                  ", North=" + self.north + ", east=" + self.east +
                  ", south=" + self.south + ", direction="+str(self.direction))
        return retVal

    @staticmethod
    def isPair(tile, candidate):
        '''Returns True if self and candidate make a pair.'''
        if tile[:-1] == candidate[:-1]:
            if tile[-1:] == "+" and candidate[-1:] == "-":
                return True
            if tile[-1:] == "-" and candidate[-1:] == "+":
                return True
        return False

    @staticmethod
    # Generalized match method that handles edge cells or those who's neighbors
    # haven't been placed. It returns the set of all possible matches including
    # rotations of the same tile.
    def match(north, west, east, south, candidates):
        '''Returns the set of tile from candidates that matches neighbors'''
        matches = []
        for item in candidates:
            start = item.direction
            while True:
                if ((north is None or Tile.isPair(north.south, item.north)) and
                    (west is None or Tile.isPair(west.east, item.west)) and 
                    (east is None or Tile.isPair(east.west, item.east)) and
                    (south is None or Tile.isPair(south.north, item.south))):
                    matches.append(Tile(item))
                item.rotate()
                if item.direction == start:
                    break;
        return matches

    def rotate(self):
        '''Rotates the tile counter clockwise '''
        temp = self.west
        self.west = self.north
        self.north = self.east
        self.east = self.south
        self.south = temp
        self.direction += 1
        if self.direction > 3:
            self.direction = 0

    def popByName(self, rest):
        if self is not None:
            idx = next((i for i, item in enumerate(rest) if item.name == self.name), None)
            if idx != None:
                rest.pop(idx)
        return rest

class Board:
    def __init__(self, param=None):
        if isinstance(param, Board):
            self.copy_constructor(param)
        elif param is None:
            self.non_copy_constructor()

    def copy_constructor(self, orig):
        self.board = orig.board.copy()
        self.row = orig.row
        self.col = orig.col
        self.items = orig.items.copy()

    def non_copy_constructor(self):
        # Start with an empty board
        self.board = [[None, None, None],[None, None, None],[None, None, None]]
        self.row = 0
        self.col = 0

    def next(self):
        '''Advances to next cell on board with wrap around'''
        self.col += 1
        if self.col > 2:
            self.col = 0
            self.row += 1
            if self.row > 2:
                self.row = 0

    # Safe getters that return None rather than exception
    def getNorth(self):
        retVal = None
        if self.row > 0:
            retVal = self.board[self.row - 1][self.col]
        return retVal

    def getSouth(self):
        retVal = None
        if self.row < 2:
            retVal = self.board[self.row + 1][self.col]
        return retVal

    def getEast(self):
        retVal = None
        if self.col < 2:
            retVal = self.board[self.row][self.col + 1]
        return retVal

    def getWest(self):
        retVal = None
        if self.col > 0:
            retVal = self.board[self.row][self.col - 1]
        return retVal

    def solve(self, depth=0):
        # Check for recursion bottoming out.
        if len(self.items) == 0:
            print("*** Puzzle Solved! ***")
            return True

        # Get the list of match for current cell and board state.
        matches = Tile.match(self.getNorth(),
                             self.getWest(),
                             self.getEast(),
                             self.getSouth(),
                             self.items)

        # What are we trying to solve now?
        print("  " * depth + "cell = (" + str(self.row) + "," + str(self.col) +
              "), items = " + str(len(self.items)) +
              ", matches = " + str(len(matches)))

        # Try each possible solution.
        for match in matches:
            print("  " * depth + "tile = " + str(match))

            # clone the current state to allow back tracking
            clone = Board(self)
            clone.board[self.row][self.col] = match
            match.popByName(clone.items)
            clone.next()
            retVal = clone.solve(depth+1)
 
           # Are we done?
            if retVal == True:
                self.board = clone.board
                return True

        # if we got here no path we tried worked.
        return False

    def print(self):
        for row in self.board:
            text = ""
            for item in row:
                if item == None:
                    text += "None,\t\t"
                else:
                    text += "name=" + item.name + " dir=" + str(item.direction) + ",\t"
            print(text)

# Load and parse the file

with open(sys.argv[1]) as f:
  data = json.load(f)

# Parse the json into array of tiles
tiles = []
for item in data:
    tiles.append( Tile(item) )

board = Board()
board.items = tiles
board.solve()
board.print()
