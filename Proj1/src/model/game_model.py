from copy import deepcopy
from enum import Enum


class Direction(Enum):
    UP = 0,
    DOWN = 1,
    LEFT = 2,
    RIGHT = 3


class Position:
    def __init__(self, row, column):
        self.__row = row
        self.__column = column

    def move(self, direction):
        if direction == Direction.UP:
            return Position(self.row - 1, self.column)
        elif direction == Direction.DOWN:
            return Position(self.row + 1, self.column)
        elif direction == Direction.LEFT:
            return Position(self.row, self.column - 1)
        elif direction == Direction.RIGHT:
            return Position(self.__row, self.column + 1)

    @property
    def row(self):
        return self.__row

    @property
    def column(self):
        return self.__column

    def __str__(self) -> str:
        return "({0}, {1})".format(self.row, self.column)

    def __hash__(self) -> int:
        return (self.row, self.column).__hash__()

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Position) and self.row == __o.row and self.column == __o.column

    def __ne__(self, __o: object) -> bool:
        return not (self == __o)


class Maze:
    def __init__(self, size, init_robot_pos, objective_pos, wall_list):
        self.__size = size
        self.__objective_pos = objective_pos
        self.__init_robot_pos = init_robot_pos
        self.__current_robot_pos = init_robot_pos
        self.__walls = {}
        for wall in wall_list:
            self.add_wall(wall)

    def can_move(self, orig, direction):
        if not self.wall_between(orig, orig.move(direction)):
            if direction == Direction.LEFT and orig.column > 0:
                return True
            elif direction == Direction.RIGHT and orig.column < (self.__size - 1):
                return True
            elif direction == Direction.UP and orig.row > 0:
                return True
            elif direction == Direction.DOWN and orig.row < (self.__size - 1):
                return True
        return False

    def possible_moves(self, orig):
        return [direction for direction in Direction if self.can_move(orig, direction)]

    def wall_between(self, orig, dest):
        return (orig in self.__walls and dest in self.__walls[orig]) or (
                    dest in self.__walls and orig in self.__walls[dest])

    def move_robot(self, dest):
        if not self.can_move(self.__current_robot_pos, dest):
            return self.__current_robot_pos
        self.__current_robot_pos = dest
        return dest

    def is_final(self):
        return self.__robot_pos == self.__objective_pos

    def add_wall(self, wall):
        if wall[0] in self.__walls:
            self.__walls[wall[0]].add(wall[1])
        elif wall[1] in self.__walls:
            self.__walls[wall[1]].add(wall[0])
        else:
            self.__walls[wall[0]] = set([wall[1]])

    def remove_wall(self, wall):
        if wall[0] in self.__walls:
            self.__walls[wall[0]].remove(wall[1])
        elif wall[1] in self.__walls:
            self.__walls[wall[1]].remove(wall[0])

    @property
    def init_robot_pos(self):
        return self.__init_robot_pos

    @init_robot_pos.setter
    def init_robot_pos(self, new_init_robot_pos):
        self.__init_robot_pos = Position(new_init_robot_pos[0], new_init_robot_pos[0])

    @property
    def final_robot_pos(self):
        return self.__objective_pos

    @final_robot_pos.setter
    def final_robot_pos(self, new_final_pos):
        self.__objective_pos = Position(new_final_pos[0], new_final_pos[1])

    @property
    def size(self):
        return self.__size

    @property
    def walls(self):
        return self.__walls

    @property
    def current_robot_pos(self):
        return self.__current_robot_pos


class GameModel:
    def __init__(self, id, maze: Maze, no_moves: int):
        self.__id = id
        self.__no_moves: int = no_moves
        self.__maze: Maze = maze
        self.__victory = False

    def simulate(self, moves):
        positions = set()
        robot_pos = self.__maze.init_robot_pos
        robot_path = [robot_pos]
        while True:
            init_cycle_pos = deepcopy(robot_pos)
            positions.add(init_cycle_pos)
            for direction in moves:
                if self.__maze.can_move(robot_pos, direction):
                    robot_pos = robot_pos.move(direction)
                    robot_path.append(robot_pos)
                if robot_pos == self.__maze.final_robot_pos:
                    return True, robot_path
            if robot_pos in positions:
                return False, robot_path

    @property
    def id(self):
        return self.__id

    @property
    def no_moves(self):
        return self.__no_moves

    @no_moves.setter
    def no_moves(self, new_no_moves):
        self.__no_moves = new_no_moves

    @property
    def maze(self):
        return self.__maze

    @property
    def victory(self):
        return self.__victory

    def toggle_won(self):
        if self.__victory:
            self.__victory = False
        else:
            self.__victory = True

    def __hash__(self) -> int:
        return self.__id
    
    def __eq__(self, __o: object) -> bool:
        return self.__id == __o.id

    def __ne__(self, __o: object) -> bool:
        return not (self == __o)
