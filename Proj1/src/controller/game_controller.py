import pygame
from copy import deepcopy

from algorithms.algorithm_stats import AlgorithmStats
from view.animator import RobotAnimator
from view.game_view import GameView, IAView
from model.game_model import Direction, GameModel

class Controller:

    def __init__(self, surface: pygame.Surface, game_model: GameModel, algorithm):
        self._surface = surface
        self._algorithm = algorithm
        self._game_model = game_model
        self._robot_animator = None
        self._moves = []

    def run(self):
        pass

    def simulate(self):
        positions = set()
        robot_pos = self._game_model.maze.init_robot_pos
        maze = self._game_model.maze
        animator = self._robot_animator
        moves = self._moves
        robot_path = [robot_pos]
        while True:
            init_cycle_pos = deepcopy(robot_pos)
            positions.add(init_cycle_pos)
            for direction in moves:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_BACKSPACE] or keys[pygame.K_ESCAPE]:
                    return
                
                if maze.can_move(robot_pos, direction):
                    animator.move_animation(robot_pos, direction)
                    robot_pos = robot_pos.move(direction)
                    robot_path.append(robot_pos)
                else:
                    animator.cancel_animation(robot_pos, direction)
                if robot_pos == maze.final_robot_pos:
                    # Win
                    self._game_model.toggle_won()
                    return
                pygame.time.delay(100)
            if robot_pos in positions:
                # Cyclycal
                return
            pygame.time.wait(300)

    def game_win(self):
        while True:
            pygame.event.wait()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] or keys[pygame.K_BACKSPACE] or keys[pygame.K_RETURN]:
                self._game_model.toggle_won()
                return



class IAController(Controller):

    def __init__(self, surface: pygame.Surface, game_model: GameModel, algorithm):
        super().__init__(surface, game_model, algorithm)
        self.__ia_view = IAView(surface, (game_model, [], AlgorithmStats(0, 0, None)))
        self._robot_animator: RobotAnimator = RobotAnimator(surface, self.__ia_view.maze_view, self.__ia_view)

    def run(self):

        results: AlgorithmStats = self._algorithm(self._game_model)
        self._moves = results.solution_state.moves
        
        self.__ia_view.update((self._game_model, self._moves, results))
        self.__ia_view.draw_static()
        self.__ia_view.draw_dynamic(self._game_model.maze.init_robot_pos)
        pygame.display.update()

        self.simulate()
        self.game_win()


        


class GameController(Controller):

    def __init__(self, surface: pygame.Surface, game_model: GameModel, algorithm):
        super().__init__(surface, game_model, algorithm)
        self.__game_view: GameView = GameView(surface, (game_model, []))
        self._robot_animator: RobotAnimator = RobotAnimator(surface, self.__game_view.maze_view, self.__game_view)
        self.__results = None

    def run(self):

        running = True
        while running:
            
            self.__game_view.draw_static()
            self.__game_view.draw_dynamic(self._game_model.maze.init_robot_pos)
            
            pygame.display.update()
            pygame.event.wait()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            keys = pygame.key.get_pressed()
            key_vals = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_BACKSPACE, pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_t, pygame.K_i]
            directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
            for i in range(9):
                if keys[key_vals[i]] or (self.__game_view.mouse_in_button(i) and pygame.mouse.get_pressed()[0]):
                    if i < 4 and len(self._moves) < self._game_model.no_moves:
                        self._moves.append(directions[i])
                        self.__game_view.update((self._game_model, self._moves))
                    elif i == 4 and len(self._moves) > 0:
                        self._moves.pop()
                    elif i == 5 and len(self._moves) == self._game_model.no_moves:
                        self.simulate()
                    elif i == 6:
                        return
                    elif i == 7:
                        self.tips()
                    elif i == 8:
                        self.instructions()

            if self._game_model.victory:
                self.game_win()
                break


    def game_win(self):
        self.__game_view.draw_win()
        pygame.display.update()
        super().game_win()

    def tips(self):
        index = 1
        wrong = False
        if self.__results is None:
            self.__results: AlgorithmStats = self._algorithm(self._game_model)
        for i in range(len(self._moves)):
            if self._moves[i] != self.__results.solution_state.moves[i]:
                wrong = True
                break
            index = i + 1
        if wrong:
            self.__game_view.tips("Change the direction number {}".format(index))
        elif len(self._moves) != self._game_model.no_moves:
            self.__game_view.tips("Add more moves")
        else:
            self.__game_view.tips("You might have done it")
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] or keys[pygame.K_BACKSPACE] or keys[pygame.K_RETURN]:
                return

    def instructions(self):
        self.__game_view.instructions()
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] or keys[pygame.K_BACKSPACE] or keys[pygame.K_RETURN]:
                return

                


