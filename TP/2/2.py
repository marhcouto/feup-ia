from queue import Queue
from puzzle_state import State


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

    print("\nPath:")
    while cur_state is not None:
        print(cur_state)
        cur_state = cur_state.parent   


def bfs(puzzle):

    q = Queue()
    s = set()

    size = len(puzzle)
    zero = find_zero(puzzle, size)

    starting_state = State(puzzle, zero, None)
    final_matrix = final_state_matrix(size)

    q.put(starting_state)
    s.add(starting_state)

    while True:

        if q.empty():
            print("Empty queue")
            return 

        cur_state = q.get()

        if cur_state.matrix == final_matrix:
            print("Success")
            break

        funcs = ['zero_up', 'zero_down', 'zero_right', 'zero_left']
        for func in funcs:
            temp = getattr(cur_state, func)()
            if temp is not None and temp not in s:
                q.put(temp)
                s.add(temp)
    
    print_path(cur_state)



if __name__ == '__main__':

    print('Starting things up')

    puzzle_a = [[1,2,3],
                [5,0,6],
                [4,7,8]]
    print("Puzzle A:\n", puzzle_a, '\n')

    bfs(puzzle_a)


    puzzle_b = [[1,3,6],
                [5,2,0],
                [4,7,8]]
    print(puzzle_b)
    puzzle_c = [[1,6,2],
                [5,7,3],
                [0,4,8]]
    print(puzzle_c)            
    puzzle_d = [[5,1,3,4],
                [2,0,7,8],
                [10,6,11,12],
                [9,13,14,15]]
    print(puzzle_d)
