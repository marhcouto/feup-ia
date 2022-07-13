import pygame
import pygame_menu

WINDOW_SIZE = (1200, 760)
SURFACE = pygame.display.set_mode(WINDOW_SIZE)

SQUARE_WIDTH = 70
ARROW_WIDTH = 40
BACKGROUND = (0, 0, 0)
COLOR = (255, 255, 255)
BLUE = (50, 0, 150)
GREEN = (50, 150, 150)
RED = (250, 0, 50)
GREY = (100, 100, 100)
BACK_SPACE = pygame.transform.scale(pygame.image.load('./assets/img/backspace.png'), (35, 35))
ROBOT = pygame.transform.scale(pygame.image.load('./assets/img/robot.png'), (SQUARE_WIDTH, SQUARE_WIDTH))
UP_ARROW = pygame.transform.scale(pygame.image.load('./assets/img/arrow_up.png'), (ARROW_WIDTH, ARROW_WIDTH))
DOWN_ARROW = pygame.transform.scale(pygame.image.load('./assets/img/arrow_down.png'), (ARROW_WIDTH, ARROW_WIDTH))
RIGHT_ARROW = pygame.transform.scale(pygame.image.load('./assets/img/arrow_right.png'), (ARROW_WIDTH, ARROW_WIDTH))
LEFT_ARROW = pygame.transform.scale(pygame.image.load('./assets/img/arrow_left.png'), (ARROW_WIDTH, ARROW_WIDTH))
ENTER = pygame.transform.scale(pygame.image.load('./assets/img/enter.png'), (ARROW_WIDTH, ARROW_WIDTH))
ESC = pygame.transform.scale(pygame.image.load('./assets/img/esc.png'), (60, 60))
TIPS = pygame.transform.scale(pygame.image.load('./assets/img/light.png'), (60, 60))
INFO = pygame.transform.scale(pygame.image.load('./assets/img/info.png'), (60, 60))
BUTTON_WIDTH = 40
THEME = pygame_menu.Theme(background_color=(0, 0, 0),
                title_background_color=(50, 0, 150))