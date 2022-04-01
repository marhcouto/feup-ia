from copy import copy, deepcopy
from types import TracebackType


class GameState:

    def __init__(self, matrix, player, lastMove, parent):
        self.matrix = matrix
        self.player = player
        self.lastMove = lastMove
        self.parent = parent



    def initialState():
        return GameState([['E','E','E','E','E','E','E'], 
                    ['E','E','E','E','E','E','E'],
                    ['E','E','E','E','E','E','E'],
                    ['E','E','E','E','E','E','E'],
                    ['E','E','E','E','E','E','E'],
                    ['E','E','E','E','E','E','E']], 'RED', (-1, -1), None)



    def placeRed(self, x):
        if x < 0 or x >= 7 or self.player != 'RED':
            return None
        newMatrix = deepcopy(self.matrix)
        for i in range(5, -1, -1):
            if newMatrix[i][x] == 'E':
                newMatrix[i][x] = 'R'
                return GameState(newMatrix, 'YELLOW', (x, i), self)

        return None



    def placeYellow(self, x):
        if x < 0 or x >= 7 or self.player != 'YELLOW':
            return None
        newMatrix = deepcopy(self.matrix)
        for i in range(5, -1, -1):
            if newMatrix[i][x] == 'E':
                newMatrix[i][x] = 'Y'
                return GameState(newMatrix, 'RED', (x, i), self)
        return None



    def nlines4(self, player):
        piece = 'R' if player == 'RED' else 'Y'
        res = 0

        # HORIZONTAL
        for i in range(0, 6):
            count = 0
            streak = False
            for j in range(0, 7):
                if self.matrix[i][j] == piece:
                    if streak:
                        count += 1
                    else:
                        count = 1
                        streak = True
                else:
                    streak = False
                    count = 0
                if count == 4:
                    res += 1
                    streak = False

        # VERTICAL
        for i in range(0, 7):
            count = 0
            streak = False
            for j in range(0, 6):
                if self.matrix[j][i] == piece:
                    if streak:
                        count += 1
                    else:
                        count = 1
                        streak = True
                else:
                    streak = False
                    count = 0
                if count == 4:
                    res += 1
                    streak = False

        # DIAGONAL
        for i in range(0, 3):
            for j in range(0, 7):
                if j > 2:
                    streak = True
                    for x in range(0, 4):
                        if self.matrix[i+x][j-x] != piece:
                            streak = False
                            break
                    if streak:
                        res += 1
                if j < 4:
                    streak = True
                    for x in range(0, 4):
                        if self.matrix[i+x][j+x] != piece:
                            streak = False
                            break
                    if streak:
                        res += 1
                        
        return res


    
    def nlines3(self, player):
        piece = 'R' if player == 'RED' else 'Y'
        res = 0

        # HORIZONTAL
        for i in range(0, 6):
            count = 0
            streak = False
            for j in range(0, 7):
                if self.matrix[i][j] == piece:
                    if streak:
                        count += 1
                    else:
                        count = 1
                        streak = True
                else:
                    streak = False
                    count = 0
                if count == 3:
                    res += 1
                    streak = False

        # VERTICAL
        for i in range(0, 7):
            count = 0
            streak = False
            for j in range(0, 6):
                if self.matrix[j][i] == piece:
                    if streak:
                        count += 1
                    else:
                        count = 1
                        streak = True
                else:
                    streak = False
                    count = 0
                if count == 3:
                    res += 1
                    streak = False

        # DIAGONAL
        for i in range(0, 3):
            for j in range(0, 7):
                if j > 2:
                    streak = True
                    for x in range(0, 3):
                        if self.matrix[i+x][j-x] != piece:
                            streak = False
                            break
                    if streak:
                        res += 1
                if j < 4:
                    streak = True
                    for x in range(0, 3):
                        if self.matrix[i+x][j+x] != piece:
                            streak = False
                            break
                    if streak:
                        res += 1
        
        return res



    def central(self, player):
        piece = 'R' if player == 'RED' else 'Y'
        res = 0

        for i in range(0,6):
            if self.matrix[i][3] == piece:
                res += 2
            if self.matrix[i][2] == piece:
                res += 1
            if self.matrix[i][4] == piece:
                res += 1

        return res



    def __eq__(self, other):
        return self.matrix == other.matrix and self.player == other.player 


    def __hash__(self):
        return hash(str(self.matrix))


    def __str__(self):
        string = ""
        for array in self.matrix:
            string += str(array) + "\n"
        return string
        