# This program solves the scrambled squares puzzle where the puzzle pieces
# must be arranged in a 3 x 3 grid with the images on the edges lined up
# correctly (e.g. the top mating with the corresponding bottom).
# This puzzle is deceptively hard to solve as the tiles can be rotated as
# well as permuated. This means there are 4^9 * 9! combinations, although
# only around 10,000 are valid.

import json
import sys

class Tile:
    def __init__(self, json):
        self.name = json["name"]
        self.west = json["west"]
        self.north = json["north"]
        self.east = json["east"]
        self.south = json["south"]
        self.direction = 0

    @staticmethod
    def isPair(tile, candidate):
        '''Returns True if self and candidate make a pair.'''
        if tile[:-1] == candidate[:-1]:
            if tile[-1:] == "+" and candidate[-1:] == "-":
                return True
            if tile[-1:] == "-" and candidate[-1:] == "+":
                return True
        return False

    def matchEast(self, candidates):
        '''Returns the first tile from candidates that is a pair to the East'''
        for item in candidates:
            start = item.direction
            while True:
                if Tile.isPair(self.east, item.west):
                    return item
                item.rotate()
                if item.direction == start:
                    break;
        return None

    def matchSouth(self, candidates):
        '''Returns the first tile from candidates that is a pair to the South'''
        for item in candidates:
            start = item.direction
            while True:
                if Tile.isPair(self.south, item.north):
                    return item
                item.rotate()
                if item.direction == start:
                    break;
        return None

    @staticmethod
    def matchNorthAndWest(north, west, candidates):
        '''Returns the first tile from candidates that is a pair to the South'''
        if north is not None and west is not None:
            for item in candidates:
                start = item.direction
                while True:
                    if (Tile.isPair(north.south, item.north) and
                        Tile.isPair(west.east, item.west)):
                        return item
                    item.rotate()
                    if item.direction == start:
                        break;
        return None

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

    def print(self):
        print("Name=" + self.name + ", west=" + self.west + ", North=" + self.north + ", east=" + self.east + ", south=" + self.south + ", direction="+str(self.direction))

class Board:
    def __init__(self, orig=None):
        if orig is None:
            self.non_copy_constructor()
        else:
            self.copy_constructor(orig)

    def non_copy_constructor(self):
        # Start with an empty board
        self.board = [[None, None, None],[None, None, None],[None, None, None]]
        self.row = 0
        self.col = 0

    def copy_constructor(self, orig):
        self.board = orig.board.copy()
        self.row = orig.row
        self.col = orig.col

    def print(self):
        for row in self.board:
            text = ""
            for item in row:
                if item == None:
                    text += "None, "
                else:
                    text += "name=" + item.name + " dir=" + str(item.direction) + ", "
            print(text)

    def incCol(self):
        self.col += 1
        if self.col > 2:
            self.col = 0
            self.row += 1
            if self.row > 2:
                return False
        return True

    def solve(self, items):
        clone = Board(self)
        items2 = items.copy()
        while clone.solveOne(items2):
            print(len(items2))
        if len(items2) != 0:
            print("Backtracing needed")
            return False
        else:
            return True

    def solveOne(self, items):
        # first row is special case a there's nothing to the north
        if self.row == 0:
            if self.col == 0:
                # fill in the corner cell which always matches.
                self.board[0][0] = items[0]
                items.pop(0)
                return self.incCol()
            else:
                match = self.board[0][self.col-1].matchEast(items)
                if match is not None:
                    self.board[0][self.col] = match
                    match.popByName(items)
                    return self.incCol()
        elif self.col == 0:
            # First column is a special case as there's nothing west.
            match = self.board[self.row-1][0].matchSouth(items)
            if match is not None:
                self.board[self.row][0] = match
                match.popByName(items)
                return self.incCol()
        else:
            # complete the rest of row
            match = Tile.matchNorthAndWest(self.board[self.row-1][self.col],
                                           self.board[self.row][self.col-1],
                                           items)
            if match is not None:
                self.board[self.row][self.col] = match
                match.popByName(items)
                return self.incCol()
        return False

# Load and parse the file

with open(sys.argv[1]) as f:
  data = json.load(f)

# Parse the json into array of tiles
tiles = []
for item in data:
    tiles.append( Tile(item) )

board = Board()
board.solve(tiles)
board.print()
