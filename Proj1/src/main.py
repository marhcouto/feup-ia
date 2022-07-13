import pygame

from menu.main_menu import MainMenu
from view.view_const import WINDOW_SIZE, SURFACE


def main():
    pygame.init()
    main_menu = MainMenu(WINDOW_SIZE).main_menu

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break

        if main_menu.is_enabled():
            main_menu.update(events)
            main_menu.draw(SURFACE)
            
        pygame.display.update()


if __name__ == '__main__':
    main()
