from algorithms.algorithms import State


class AlgorithmStats:
    def __init__(self, time: float, iterations: int, solution_state: State):
        self.__time = time
        self.__iterations = iterations
        self.__solution_state = solution_state

    @property
    def time(self):
        return self.__time

    @property
    def iterations(self):
        return self.__iterations

    @property
    def solution_state(self):
        return self.__solution_state

    @property
    def solution_history(self):
        return [state for state in map(lambda x: x.moves, self.__solution_state.build_state_history())]
