import model.sample_mazes as sample_mazes
import algorithms.algorithms
import algorithms.heuristic
from algorithms.heuristic import force_shortest_path_cache
from model.game_model import Direction


__solutions = [
    (Direction.UP, Direction.UP, Direction.DOWN, Direction.RIGHT),
    (Direction.RIGHT, Direction.RIGHT, Direction.LEFT, Direction.UP),
    (Direction.RIGHT, Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.UP),
    (Direction.RIGHT, Direction.UP, Direction.RIGHT, Direction.LEFT, Direction.UP),
    (Direction.RIGHT, Direction.DOWN, Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.UP),
    (Direction.UP, Direction.RIGHT, Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.UP)    
]

__mazes = [
    sample_mazes.LEVEL_1,
    sample_mazes.LEVEL_2,
    sample_mazes.LEVEL_4,
    sample_mazes.LEVEL_6,
    sample_mazes.LEVEL_8,
    sample_mazes.LEVEL_12
]

__algorithms = [
    ('bfs', algorithms.algorithms.breadth_first_search),
    ('dfs', algorithms.algorithms.depth_first_search),
    ('iddfs', algorithms.algorithms.iterative_deepening_search),
    ('greedy_manhattan', lambda game_state: algorithms.algorithms.greedy_search(game_state,algorithms.heuristic.manhattan_distance)),
    ('a_star_manhattan', lambda game_state: algorithms.algorithms.a_star_search(game_state, algorithms.heuristic.manhattan_distance)),
    ('greedy_manhattan_div_distance', lambda game_state: algorithms.algorithms.greedy_search(game_state, algorithms.heuristic.manhattan_distance_div_dist)),
    ('a_star_manhattan_div_distance', lambda game_state: algorithms.algorithms.a_star_search(game_state, algorithms.heuristic.manhattan_distance_div_dist)),
    ('greedy_shortest_path', lambda game_state: algorithms.algorithms.greedy_search(game_state, algorithms.heuristic.shortest_path_heuristic)),
    ('a_star_shortest_path', lambda game_state: algorithms.algorithms.a_star_search(game_state, algorithms.heuristic.shortest_path_heuristic)),
    ('greedy_max_dist', lambda game_state: algorithms.algorithms.greedy_search(game_state, algorithms.heuristic.greatest_axis_distance)),
    ('a_star_max_dist', lambda game_state: algorithms.algorithms.a_star_search(game_state, algorithms.heuristic.greatest_axis_distance)),
    ('greedy_max_dist_div_distance', lambda game_state: algorithms.algorithms.greedy_search(game_state, algorithms.heuristic.greatest_axis_distance_div_dist)),
    ('a_star_max_dist_div_distance', lambda game_state: algorithms.algorithms.a_star_search(game_state, algorithms.heuristic.greatest_axis_distance_div_dist))
]

def test():
    #Forces caching of shortest path data to improve benchmark accuracy
    for game_model in __mazes:
        force_shortest_path_cache(game_model)
    for i in range(len(__mazes)):
            for algorithm in __algorithms:
                algorithm_stats = algorithm[1](__mazes[i])
                if algorithm_stats.solution_state.moves != __solutions[i]:
                    print("Test failed with algorithm {} and maze {}".format(algorithm[0], __mazes[i].id))
                    exit(1)
    print("Tests passed")

if __name__ == '__main__':
    test()

