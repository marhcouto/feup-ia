import pygame_menu
from menu.instructions_menu import IntructionsMenu

from menu.maze_selector_menu import MazeSelectorMenu
from view.view_const import THEME


class MainMenu:
    def __init__(self, window_size):
        self.__main_menu = pygame_menu.Menu(
            height=window_size[1],
            width=window_size[0],
            title='Main Menu',
            theme=THEME
        )
        self.__main_menu.add.image('./assets/img/robot_image.png', scale=(0.5, 0.5))
        self.__main_menu.add.button('Choose Map', MazeSelectorMenu(window_size).maze_selector_menu)
        self.__main_menu.add.button('Instructions', IntructionsMenu(window_size).menu)
        self.__main_menu.add.button('Quit', pygame_menu.events.EXIT)

    @property
    def main_menu(self):
        return self.__main_menu
