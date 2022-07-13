import pygame
import pygame_menu

import algorithms.algorithms
import algorithms.heuristic
from model.sample_mazes import IMPOSSIBLE_LEVEL, LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5, LEVEL_6, LEVEL_7, LEVEL_8, LEVEL_9, LEVEL_10, LEVEL_11, LEVEL_12, SAMPLE_LEVEL, LEVEL_13
from view.game_view import MazeView
from view.view_const import BACKGROUND, SURFACE, THEME
from controller.game_controller import GameController, IAController


class MazeSelectorMenu:
    def __init__(self, window_size):
        self.__window_size = window_size
        self.__maze_surface = pygame.Surface((550, 550))
        self.__maze_selector_menu = pygame_menu.Menu(
            height=self.__window_size[1],
            width=self.__window_size[0],
            title='Choose a maze',
            columns=2,
            rows=4,
            theme=THEME
        )
        self.__mazes = [
            ('Sample(4x4) 4', SAMPLE_LEVEL),
            ('Level 1', LEVEL_1),
            ('Level 2', LEVEL_2),
            ('Level 3', LEVEL_3),
            ('Level 4', LEVEL_4),
            ('Level 5', LEVEL_5),
            ('Level 6', LEVEL_6),
            ('Level 7', LEVEL_7),
            ('Level 8', LEVEL_8),
            ('Level 9', LEVEL_9),
            ('Level 10', LEVEL_10),
            ('Level 11', LEVEL_11),
            ('Level 12', LEVEL_12),
            ('Level 13', LEVEL_13),
            ('Impossible level', IMPOSSIBLE_LEVEL)
        ]
        #Each algorithm expects a game_state
        #Because greedy and a* need heuristics we use a lambda to curry a 2 argument function that expects a game_model and heuristic into a single argument function that only expects the game_model
        self.__algorithms = [
            ('Breadth-First Search', algorithms.algorithms.breadth_first_search),
            ('Depth-First Search', algorithms.algorithms.depth_first_search),
            ('Iterative Deepening DFS', algorithms.algorithms.iterative_deepening_search),
            ('Greedy(Manhattan)', lambda game_state: algorithms.algorithms.greedy_search(game_state,algorithms.heuristic.manhattan_distance)),
            ('A*(Manhattan)', lambda game_state: algorithms.algorithms.a_star_search(game_state, algorithms.heuristic.manhattan_distance)),
            ('Greedy(Manhattan/Distance)', lambda game_state: algorithms.algorithms.greedy_search(game_state, algorithms.heuristic.manhattan_distance_div_dist)),
            ('A*(Manhattan/Distance)', lambda game_state: algorithms.algorithms.a_star_search(game_state, algorithms.heuristic.manhattan_distance_div_dist)),
            ('Greedy(Shortest Path)', lambda game_state: algorithms.algorithms.greedy_search(game_state, algorithms.heuristic.shortest_path_heuristic)),
            ('A*(Shortest Path)', lambda game_state: algorithms.algorithms.a_star_search(game_state, algorithms.heuristic.shortest_path_heuristic)),
            ('Greedy(MaxDist)', lambda game_state: algorithms.algorithms.greedy_search(game_state, algorithms.heuristic.greatest_axis_distance)),
            ('A*(MaxDist)', lambda game_state: algorithms.algorithms.a_star_search(game_state, algorithms.heuristic.greatest_axis_distance)),
            ('Greedy(MaxDist/Distance)', lambda game_state: algorithms.algorithms.greedy_search(game_state, algorithms.heuristic.greatest_axis_distance_div_dist)),
            ('A*(MaxDist/Distance)', lambda game_state: algorithms.algorithms.a_star_search(game_state, algorithms.heuristic.greatest_axis_distance_div_dist))
        ]
        self.__cur_maze = 0
        self.__cur_algorithm = 0
        self.__widget_list = []
        self.__update_widgets()

    def __change_maze(self):
        self.__cur_maze = self.__maze_widget.get_index()
        if not self.__updating_widgets:
            self.__update_widgets()
        if self.mazes[self.__cur_maze][1]:
            maze_view = MazeView(self.__maze_surface, self.mazes[self.__cur_maze][1].maze)
            maze_view.draw_static()
            maze_view.draw_dynamic(self.mazes[self.__cur_maze][1].maze.init_robot_pos)
        else:
            self.__maze_surface.fill((255, 255, 255))

    def __change_algorithm(self):
        self.__cur_algorithm = self.__algorithm_widget.get_index()
        if not self.__updating_widgets:
            self.__update_widgets()

    def __update_widgets(self):
        self.__updating_widgets = True
        for widget in self.__widget_list:
            self.maze_selector_menu.remove_widget(widget)
        self.__widget_list = []
        self.__maze_widget = self.maze_selector_menu.add.selector(
            title='Maze: ',
            items=self.mazes,
            onchange=lambda _, __: self.__change_maze(),
            default=self.__cur_maze
        )
        self.__algorithm_widget = self.maze_selector_menu.add.dropselect(
            title='Algorithm: ',
            items=self.algorithms,
            onchange=lambda _, __: self.__change_algorithm(),
            default=self.__cur_algorithm
        )
        ia_menu = IAController(SURFACE, self.mazes[self.__cur_maze][1], self.algorithms[self.__cur_algorithm][1]).run
        play_menu = GameController(SURFACE, self.mazes[self.__cur_maze][1], self.algorithms[self.__cur_algorithm][1]).run
        self.__maze_surface.fill(BACKGROUND)
        next_button = self.maze_selector_menu.add.button('Simulate', ia_menu)
        play_button = self.maze_selector_menu.add.button('Play', play_menu)
        maze_surface = self.maze_selector_menu.add.surface(self.__maze_surface)
        self.__widget_list = [
            self.__maze_widget,
            self.__algorithm_widget,
            next_button,
            play_button,
            maze_surface
        ]
        if self.mazes[self.__cur_maze][1]:
            maze_view = MazeView(self.__maze_surface, self.mazes[self.__cur_maze][1].maze)
            maze_view.draw_static()
            maze_view.draw_dynamic(self.mazes[self.__cur_maze][1].maze.init_robot_pos)
        self.__updating_widgets = False

    @property
    def maze_selector_menu(self):
        return self.__maze_selector_menu

    @property
    def mazes(self):
        return self.__mazes

    @property
    def algorithms(self):
        return self.__algorithms
