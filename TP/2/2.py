from queue import Queue
from puzzle_state import State
from time import time


def final_state_matrix(size):
    matrix = list()

    for i in range(0,size):
        temp = []
        for j in range(1, size + 1):
            temp.append(i * size + j)
        matrix.append(temp)
    
    matrix[size - 1][size - 1] = 0
    return matrix
    

def find_zero(puzzle, size):
    for i in range(0, size):
        for j in range(0, size):
            if puzzle[i][j] == 0:
                return (i,j)


def print_path(final_state):
    cur_state = final_state

    print("Path:")
    while cur_state is not None:
        print(cur_state, cur_state.distance(), cur_state.depth)
        cur_state = cur_state.parent   


def bfs(puzzle):

    q = Queue()
    s = set()

    size = len(puzzle)
    zero = find_zero(puzzle, size)

    starting_state = State(puzzle, zero, None, 0)
    final_matrix = final_state_matrix(size)

    q.put(starting_state)
    s.add(starting_state)

    nodes_explored = 0
    while True:
        nodes_explored += 1

        if q.empty():
            print("Empty queue")
            return 

        cur_state = q.get()
        # print('Current state:', cur_state)

        if cur_state.matrix == final_matrix:
            print("Success")
            break

        funcs = ['zero_up', 'zero_down', 'zero_right', 'zero_left']
        for func in funcs:
            new_state = getattr(cur_state, func)()
            if new_state is not None and new_state not in s:
                q.put(new_state)
                s.add(new_state)
    
    print_path(cur_state)
    print("Nodes explored:", nodes_explored)



def aStar(puzzle):

    q = []
    s = set()
    size = len(puzzle)
    zero = find_zero(puzzle, size)

    starting_state = State(puzzle, zero, None, 0)
    final_matrix = final_state_matrix(size)

    q.append(starting_state)
    s.add(starting_state)

    nodes_explored = 0
    while True:
        nodes_explored += 1

        if len(q) == 0:
            print("Empty queue")
            return 

        # for item in q:
        #     print(item, item.distance() + item.depth, end=", ")
        cur_state = q.pop(0)
        # print('Current state:', cur_state)

        if cur_state.matrix == final_matrix:
            print("Success")
            break

        funcs = ['zero_up', 'zero_down', 'zero_right', 'zero_left']
        for func in funcs:
            new_state = getattr(cur_state, func)()
            if new_state is not None and new_state not in s:
                i = 0
                for state in q:
                    if new_state.distance() + new_state.depth > state.distance() + state.depth:
                        i += 1
                    else:
                        break
                q.insert(i, new_state)
                s.add(new_state)

    print_path(cur_state)
    print("Nodes explored:", nodes_explored)

    


if __name__ == '__main__':

    print('Starting things up')

    puzzle_a = [[1,2,3],
                [5,0,6],
                [4,7,8]]
    print("Puzzle A:\n", puzzle_a)
    bfs_starttime = time()
    bfs(puzzle_a)
    bfs_stoptime = time()
    print("BFS took {} seconds".format(bfs_stoptime - bfs_starttime))
    aStar_starttime = time()
    aStar(puzzle_a)
    aStar_stoptime = time()
    print("A* took {} seconds\n".format(aStar_stoptime - aStar_starttime))

    puzzle_b = [[1,3,6],
                [5,2,0],
                [4,7,8]]
    print("Puzzle B:\n", puzzle_b)
    bfs_starttime = time()
    bfs(puzzle_b)
    bfs_stoptime = time()
    print("BFS took {} seconds".format(bfs_stoptime - bfs_starttime))
    aStar_starttime = time()
    aStar(puzzle_b)
    aStar_stoptime = time()
    print("A* took {} seconds\n".format(aStar_stoptime - aStar_starttime))

    puzzle_c = [[1,6,2],
                [5,7,3],
                [0,4,8]]
    print("Puzzle C:\n", puzzle_c)
    bfs_starttime = time()
    bfs(puzzle_c)
    bfs_stoptime = time()
    print("BFS took {} seconds".format(bfs_stoptime - bfs_starttime))
    aStar_starttime = time()
    aStar(puzzle_c)
    aStar_stoptime = time()
    print("A* took {} seconds\n".format(aStar_stoptime - aStar_starttime))     

    puzzle_d = [[5,1,3,4],
                [2,0,7,8],
                [10,6,11,12],
                [9,13,14,15]]
    print("Puzzle D:\n", puzzle_d)
    bfs_starttime = time()
    bfs(puzzle_d)
    bfs_stoptime = time()
    print("BFS took {} seconds".format(bfs_stoptime - bfs_starttime))
    aStar_starttime = time()
    aStar(puzzle_d)
    aStar_stoptime = time()
    print("A* took {} seconds\n".format(aStar_stoptime - aStar_starttime))
