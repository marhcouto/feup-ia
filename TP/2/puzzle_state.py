from copy import copy, deepcopy


class State:
    def __init__(self, matrix, zero, parent):
        self.zero = zero
        self.matrix = matrix
        self.size = len(matrix)
        self.parent = parent

    def zero_up(self):
        if self.zero[0] == 0:
            return None
        new_zero = (self.zero[0] - 1, self.zero[1])
        new_matrix = deepcopy(self.matrix)
        new_matrix[self.zero[0]][self.zero[1]] = new_matrix[self.zero[0] - 1][self.zero[1]]
        new_matrix[self.zero[0] - 1][self.zero[1]] = 0
        return State(new_matrix, new_zero, self)

    def zero_down(self):
        if self.zero[0] == self.size - 1:
            return None
        new_zero = (self.zero[0] + 1, self.zero[1])
        new_matrix = deepcopy(self.matrix)
        new_matrix[self.zero[0]][self.zero[1]] = new_matrix[self.zero[0] + 1][self.zero[1]]
        new_matrix[self.zero[0] + 1][self.zero[1]] = 0
        return State(new_matrix, new_zero, self)

    def zero_right(self):
        if self.zero[1] == self.size - 1:
            return None
        new_zero = (self.zero[0], self.zero[1] + 1)
        new_matrix = deepcopy(self.matrix)
        new_matrix[self.zero[0]][self.zero[1]] = new_matrix[self.zero[0]][self.zero[1] + 1]
        new_matrix[self.zero[0]][self.zero[1] + 1] = 0
        return State(new_matrix, new_zero, self)

    def zero_left(self):
        if self.zero[1] == 0:
            return None
        new_zero = (self.zero[0], self.zero[1] - 1)
        new_matrix = deepcopy(self.matrix)
        new_matrix[self.zero[0]][self.zero[1]] = new_matrix[self.zero[0]][self.zero[1] - 1]
        new_matrix[self.zero[0]][self.zero[1] - 1] = 0
        return State(new_matrix, new_zero, self)

    def distance(self, other):

        for i in range(0, self.size):
            for j in range(0, self.size):

    
    def __eq__(self, other):
        return self.matrix == other.matrix

    def __hash__(self):
        return hash(str(self.matrix))

    def __str__(self):
        return str(self.matrix)