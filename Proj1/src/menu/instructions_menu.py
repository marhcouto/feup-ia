import pygame_menu

from view.view_const import THEME


class IntructionsMenu:
    def __init__(self, window_size):
        self.__menu = pygame_menu.Menu(
            height=window_size[1],
            width=window_size[0],
            title='Instructions',
            theme=THEME
        )
        self.__menu.add.image('./assets/img/description.png', scale=(1, 1))
        
    @property
    def menu(self):
        return self.__menu
