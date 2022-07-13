from model.game_model import Direction
from queue import Queue


__shortest_path_cache = {}


class MazeBFSState:
    def __init__(self, position, parent):
        self.position = position
        self.parent = parent
    
    def __hash__(self):
        return self.position.__hash__()
    
    def __eq__(self, __o):
        return self.position == __o.position


def force_shortest_path_cache(game_model):
    if (not game_model in __shortest_path_cache):
        __shortest_path_cache[game_model] = __maze_bfs(game_model.maze)


def manhattan_distance(game_model, state):
    final_pos = game_model.simulate(state.moves)[1][-1:][0]
    return abs(final_pos.row - game_model.maze.final_robot_pos.row) + abs(final_pos.column - game_model.maze.final_robot_pos.column)


def manhattan_distance_div_dist(game_model, state):
    if (not game_model in __shortest_path_cache):
        __shortest_path_cache[game_model] = __maze_bfs(game_model.maze)
    return manhattan_distance(game_model, state) / (2 * game_model.maze.size)

def generate_neighbour_positions(maze, cur_robot_pos):
    neigh = []
    for direction in Direction:
        if maze.can_move(cur_robot_pos, direction):
            neigh.append(cur_robot_pos.move(direction))
    return neigh


def __maze_bfs(maze):
    q = Queue()
    s = set()
    starting_pos = MazeBFSState(maze.init_robot_pos, None)
    cur_pos = starting_pos

    q.put(starting_pos)

    while not q.empty():
        cur_pos = q.get()
        if cur_pos.position == maze.final_robot_pos:
            break

        children = generate_neighbour_positions(maze, cur_pos.position)
        #Creates MazeBFSState from simple Position objects 
        children = [child for child in map(lambda child_pos: MazeBFSState(child_pos, cur_pos), children)]
        for child in children:
            if not (child in s):
                s.add(child)
                q.put(child)

    path = []
    while cur_pos.parent:
        path.append(cur_pos.position)
        cur_pos = cur_pos.parent
    path.append(cur_pos.position)
    path.reverse()
    return path


def shortest_path_heuristic(game_model, state):
    if (not game_model in __shortest_path_cache):
        __shortest_path_cache[game_model] = __maze_bfs(game_model.maze)
    shortest_path = __shortest_path_cache[game_model]
    loop_path = game_model.simulate(state.moves)[1]
    common_positions = set()
    for position in shortest_path:
        if position in loop_path:
            common_positions.add(position)
    return len(shortest_path) - len(common_positions)


def greatest_axis_distance(game_model, state):
    final_pos = game_model.simulate(state.moves)[1][-1:][0]
    return max(abs(final_pos.row - game_model.maze.final_robot_pos.row), abs(final_pos.column - game_model.maze.final_robot_pos.column))


def greatest_axis_distance_div_dist(game_model, state):
    final_pos = game_model.simulate(state.moves)[1][-1:][0]
    if (not game_model in __shortest_path_cache):
        __shortest_path_cache[game_model] = __maze_bfs(game_model.maze)
    return max(abs(final_pos.row - game_model.maze.final_robot_pos.row), abs(final_pos.column - game_model.maze.final_robot_pos.column)) / game_model.maze.size