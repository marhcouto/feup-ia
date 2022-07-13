import model.sample_mazes as sample_mazes
import algorithms.algorithms
import algorithms.heuristic
from algorithms.heuristic import force_shortest_path_cache

__n_sample = 5

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

def benchmark():
    #Forces caching of shortest path data to improve benchmark accuracy
    for game_model in __mazes:
        force_shortest_path_cache(game_model)
    for maze in __mazes:
        with open('benchmark_results/{0}.csv'.format(maze.id), 'w') as f:
            f.write('Algorithm,Execution Time,Iterations,Solution Depth\n')
            for algorithm in __algorithms:
                total_exec_time = 0
                for _ in range(__n_sample):
                    algorithm_stats = algorithm[1](maze)
                    solution_depth = len(algorithm_stats.solution_history)
                    total_exec_time += algorithm_stats.time
                f.write('{0},{1:.2f},{2},{3}\n'.format(algorithm[0], total_exec_time/__n_sample, algorithm_stats.iterations, solution_depth))
