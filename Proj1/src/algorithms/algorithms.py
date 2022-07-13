import math
from queue import Queue, LifoQueue
from time import perf_counter_ns

from algorithms.state import State
from algorithms.algorithm_stats import AlgorithmStats
from algorithms.heap import Heap
from model.game_model import GameModel

# Simple breadth first search algorithm
# Each state is inserted in a FIFO
# Each state in the FIFO popped from the state queue and visited in that order until we find the solution
def breadth_first_search(game_model: GameModel) -> AlgorithmStats:
    q = Queue()
    #This set is used to avoid cycles
    s = set()
    nodes_explored = 0
    starting_state = State.initial_state(game_model.no_moves)
    cur_state: State

    q.put(starting_state)
    s.add(starting_state)

    start_time: int = perf_counter_ns()

    while True:
        if q.empty():
            cur_state = None
            break

        nodes_explored += 1

        cur_state = q.get()
        if game_model.simulate(cur_state.moves)[0]:
            break

        children = cur_state.generate_all_children()
        for child in children:
            if not (child in s):
                s.add(child)
                q.put(child)
    end_time: int = perf_counter_ns()
    time: float = (end_time - start_time) / 1000000
    return AlgorithmStats(time, nodes_explored, cur_state)

# Simple depth first search algorithm
# Each state is inserted in a LIFO
# Each state in the LIFO popped from the state stack and visited in that order until we find the solution
def depth_first_search(game_model: GameModel, max_depth=math.inf) -> AlgorithmStats:
    q = LifoQueue()
    s = set()
    nodes_explored = 0
    starting_state = State.initial_state(game_model.no_moves)
    cur_state: State

    q.put(starting_state)
    s.add(starting_state)

    start_time: int = perf_counter_ns()

    while True:
        if q.empty():
            cur_state = None
            break

        nodes_explored += 1

        cur_state = q.get()
        if game_model.simulate(cur_state.moves)[0]:
            break
        if cur_state.depth < max_depth:
            children = cur_state.generate_all_children()
            for child in children:
                if not (child in s):
                    q.put(child)
                    s.add(cur_state)

    end_time: int = perf_counter_ns()
    time: float = (end_time - start_time) / 1000000
    return AlgorithmStats(time, nodes_explored, cur_state)

# Iterative deepening depth first search algorithm
# We start with a maximum depth of 0 and increase it by one until we can find the solution using DFS
def iterative_deepening_search(game_model: GameModel) -> AlgorithmStats:
    depth = 0

    start_time: int = perf_counter_ns()

    nodes_explored = 0

    while True:
        alg_res = depth_first_search(game_model, depth)
        found: State = alg_res.solution_state
        nodes_explored += alg_res.iterations
        if found:
            break
        depth += 1

    end_time: int = perf_counter_ns()
    time: float = (end_time - start_time) / 1000000
    return AlgorithmStats(time, nodes_explored, found)

# Each node is inserted in a heap that orders the items according to the heuristic
# Then we pop a state from the queue insert it's children in the queue and repeat this process until we find a solution
def greedy_search(game_model: GameModel, heuristic):

    nodes_explored: int = 0
    visited_states = set()
    state_queue = Heap(lambda state: heuristic(game_model, state))
    state_queue.insert(State.initial_state(game_model.no_moves))
    current_state: State

    start_time: int = perf_counter_ns()
    while True:
        if state_queue.empty():
            print("Empty queue")
            current_state = None
            break

        nodes_explored += 1
        current_state = state_queue.pop()
        if game_model.simulate(current_state.moves)[0]:
            break
        new_valid_nodes = current_state.generate_all_children()
        for node in new_valid_nodes:
            if not (node in visited_states):
                state_queue.insert(node)
                visited_states.add(node)
    end_time: int = perf_counter_ns()
    time: float = (end_time - start_time) / 1000000
    return AlgorithmStats(time, nodes_explored, current_state)

# A* Algorithm
# We use a heap like in greedy algorithm but this time the value of each state in the queue is it's depth plus the value of the given heuristic 
# Then we pop a state from the queue insert it's children in the queue and repeat this process until we find a solution
def a_star_search(game_model: GameModel, heuristic):
    visited_states = set()
    node_queue = Heap(lambda state: heuristic(game_model, state))
    initial_state = State.initial_state(game_model.no_moves)
    node_queue.insert_with_custom_value(initial_state.depth + heuristic(game_model, initial_state), initial_state)
    visited_states.add(initial_state)
    cur_node: State
    iter_num = 0

    start_time: int = perf_counter_ns()

    while not node_queue.empty():
        iter_num += 1
        cur_node = node_queue.pop()
        if game_model.simulate(cur_node.moves)[0]:
            break
        next_nodes = cur_node.generate_all_children()
        for node in next_nodes:
            if node not in visited_states:
                a_star_val = node.depth + heuristic(game_model, node)
                node_queue.insert_with_custom_value(a_star_val, node)
                visited_states.add(node)

    end_time: int = perf_counter_ns()
    time: float = (end_time - start_time) / 1000000
    return AlgorithmStats(time, iter_num, cur_node)
