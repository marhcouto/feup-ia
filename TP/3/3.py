
from game_state import GameState



def game(depth, func):

    state = GameState.initialState()
    gameOver = False


    while not gameOver:

        print("\n\nState:\n{}".format(state))

        if state.player == 'RED':
            col = int(input('Choose column to play:'))
            state = state.placeRed(col)
        else:
            col = minimax(state, depth, func)
            state = state.placeYellow(col)

        if state is None:
            print('Invalid play')
            continue

        if state.nlines4('RED') >= 1:
            print('RED WON')
            gameOver = True
        elif state.nlines4('YELLOW') >= 1:
            print('YELLOW WON')
            gameOver = True



def minimax(state, depth, func):

    bestScore = -999999
    bestI = 0

    for i in range(0, 7):
        newState = state.placeYellow(i)
        if newState is None:
            continue
        newScore = minimax_aux(newState, 0, depth, func)
        if newScore > bestScore:
            bestScore = newScore
            bestI = i

    return bestI

    



def minimax_aux(state, currentDepth, maxDepth, func):


    if maxDepth == currentDepth or state.nlines4('RED') or state.nlines4('YELLOW') >= 1:
        return func(state)

    if state.player == 'RED':
        best = 99999
        for i in range(0, 7):
            newState = state.placeRed(i)
            if newState is not None:
                score = minimax_aux(newState, currentDepth + 1, maxDepth, func)
                best = best if best < score else score
    else:
        best = -99999
        for i in range(0, 7):
            newState = state.placeYellow(i)
            if newState is not None:
                score = minimax_aux(newState, currentDepth + 1, maxDepth, func)
                best = best if best > score else score

    return best 


def func1(state):
    return state.nlines4('YELLOW') - state.nlines4('RED')

def func2(state):
    return 100*func1(state) + state.nlines3('YELLOW') - state.nlines3('RED')

def func3(state):
    return 100*func1(state) + state.central('YELLOW') - state.central('RED')

def func4(state):
    return 5*func2(state) + func3(state)


if __name__ == '__main__':
    
    opt = int(input("Game option: (1,2,3 or 4)"))
    if opt == 1:
        game(4, func1)
    elif opt == 2:
        game(4, func2)
    elif opt == 3:  
        game(4, func3)
    elif opt == 4:
        game(4, func4)
    else:
        print("Invalid option")
    
