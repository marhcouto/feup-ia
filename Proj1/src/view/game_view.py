import pygame
from algorithms.algorithm_stats import AlgorithmStats

from model.game_model import Maze, Position, Direction
from view.view_utils import EdgeFactory, MazeEdge
from view.view_const import GREEN, BLUE, BACKGROUND, COLOR, INFO, BACK_SPACE, ESC, ENTER, RED, ROBOT, TIPS, SQUARE_WIDTH, ARROW_WIDTH, UP_ARROW, DOWN_ARROW, LEFT_ARROW, RIGHT_ARROW, BUTTON_WIDTH

class View:
    def __init__(self, surface: pygame.Surface, model = None):
        self._surface = surface
        self.model = model
        self._build()

    def _build(self):
        pass

    def update(self, model):
        self.model = model
        self._build()

    def draw_static(self):
        pass

    def draw_dynamic(self, **data):
        pass



class MazeView(View):

    TOP = 100

    def __init__(self, surface: pygame.Surface, maze: Maze):
        super().__init__(surface, maze)

    def row_column_to_x_y(self, position: Position):
        return (position.column * SQUARE_WIDTH + MazeView.left(self._surface, self.model), position.row * SQUARE_WIDTH + MazeView.TOP)

    @staticmethod
    def left(surface: pygame.Surface, maze: Maze):
        screen_w, _ = surface.get_size()
        return (screen_w - maze.size * SQUARE_WIDTH) // 2

    def _build(self):
        self.__left = MazeView.left(self._surface, self.model)

    def draw_static(self):
        passage: MazeEdge = EdgeFactory.no_wall()
        wall: MazeEdge = EdgeFactory.real_wall()

        # pygame.draw.rect(self._surface, COLOR, pygame.Rect(self.__left, MazeView.TOP, SQUARE_WIDTH * self.model.size, SQUARE_WIDTH * self.model.size))

        # Starting house
        (initial_x, initial_y) = (self.model.init_robot_pos.column * SQUARE_WIDTH + self.__left, self.model.init_robot_pos.row * SQUARE_WIDTH + MazeView.TOP)
        pygame.draw.rect(self._surface, BLUE, pygame.Rect(initial_x, initial_y, SQUARE_WIDTH, SQUARE_WIDTH))

        # Ending house
        (final_x, final_y) = (self.model.final_robot_pos.column * SQUARE_WIDTH + self.__left, self.model.final_robot_pos.row * SQUARE_WIDTH + MazeView.TOP)
        pygame.draw.rect(self._surface, GREEN, pygame.Rect(final_x, final_y, SQUARE_WIDTH, SQUARE_WIDTH))

        # Horizontal Lines
        for i in range(self.model.size):
            lines_y = i * SQUARE_WIDTH + MazeView.TOP
            pygame.draw.line(self._surface, passage.color, (self.__left, lines_y), (self.__left + SQUARE_WIDTH * self.model.size, lines_y), passage.width)

        # Vertical Lines
        for i in range(self.model.size):
            line_x = i * SQUARE_WIDTH + self.__left
            pygame.draw.line(self._surface, passage.color, (line_x, MazeView.TOP), (line_x, MazeView.TOP + SQUARE_WIDTH * self.model.size), passage.width)

        # Maze frame
        pygame.draw.rect(self._surface, wall.color, pygame.Rect(self.__left, MazeView.TOP, SQUARE_WIDTH * self.model.size, SQUARE_WIDTH * self.model.size), wall.width)
        
        # Walls
        for position1, positions in self.model.walls.items():
            for position2 in positions:
                # Horizontal wall
                if position1.column == position2.column:
                    if (position2.row < position1.row):
                        temp = position1
                        position1 = position2
                        position2 = temp
                    pygame.draw.line(self._surface, wall.color, (position1.column * SQUARE_WIDTH + self.__left, position2.row * SQUARE_WIDTH + MazeView.TOP),
                        ((position1.column + 1) * SQUARE_WIDTH + self.__left, position2.row * SQUARE_WIDTH + MazeView.TOP), wall.width)
                # Vertical wall
                else:
                    if (position2.column < position1.column):
                        temp = position1
                        position1 = position2
                        position2 = temp
                    pygame.draw.line(self._surface, wall.color, (position2.column * SQUARE_WIDTH + self.__left, (position1.row + 1) * SQUARE_WIDTH + MazeView.TOP),
                        (position2.column * SQUARE_WIDTH + self.__left, position1.row * SQUARE_WIDTH + MazeView.TOP), wall.width)

    def draw_dynamic(self, position: Position):
        self._surface.blit(ROBOT, self.row_column_to_x_y(position))


class MovesView(View):

    def __init__(self, surface: pygame.Surface, moves: list(Direction)):
        super().__init__(surface, moves)

    def draw_static(self):

        self._build()

        moves_string = 'Moves: {}'.format(self.model[1])

        text = pygame.font.Font(None, 48).render(moves_string, True, COLOR, BACKGROUND)
        self._surface.blit(text, (30, 10))
   
        x = 20
        y = 50

        for move in self.model[0]:
            self.__draw_move(move, (x, y))
            x += ARROW_WIDTH

    def __draw_move(self, move: Direction, position: tuple):

        if move == Direction.UP:
            self._surface.blit(UP_ARROW, position)
        elif move == Direction.DOWN:
            self._surface.blit(DOWN_ARROW, position)
        elif move == Direction.LEFT:
            self._surface.blit(LEFT_ARROW, position)
        elif move == Direction.RIGHT:
            self._surface.blit(RIGHT_ARROW, position)



class StatsView(View):

    def __init__(self, surface: pygame.Surface, results: AlgorithmStats):
        super().__init__(surface, results)

    def draw_static(self):


        if self.model is None:
            return

        data = [
            "Execution Time: {0} ms".format(self.model.time),
            "Iterations: {0}".format(self.model.iterations),
            "Solution Depth: {0}".format(len(self.model.solution_history)),
            "Found Solution: {0}".format(self.__render_solution())
        ]

        text = pygame.font.Font(None, 48).render("Algorithm Stats:", True, COLOR, BACKGROUND)
        self._surface.blit(text, (30, 200))

        y = 240
        for sentence in data:
            text = pygame.font.Font(None, 32).render(sentence, True, COLOR, BACKGROUND)
            self._surface.blit(text, (30, y))
            y += 30

    def __render_solution(self):
        res_str = "({0}".format(self.__render_direction(self.model.solution_history[-1::][0][0]))
        for direction in self.model.solution_history[-1::][0][1::]:
            res_str += ", {0}".format(self.__render_direction(direction))
        res_str += ")"
        return res_str

    @staticmethod
    def __render_direction(direction):
        if direction == Direction.UP:
            return 'U'
        elif direction == Direction.DOWN:
            return 'D'
        elif direction == Direction.LEFT:
            return 'L'
        elif direction == Direction.RIGHT:
            return 'R'



class GameView(View):

    def __init__(self, surface: pygame.Surface, model):
        super().__init__(surface, model)

    def _build(self):
        self.maze_view = MazeView(self._surface, self.model[0].maze)
        self.moves_view = MovesView(self._surface, (self.model[1], self.model[0].no_moves))
        self.buttons = [(400, 650), (450, 650), (500, 650), (550, 650), (700, 650), (750, 650), (1100, 20), (1000, 20), (900, 20)]
        self.button_widths = [40, 40, 40, 40, 40, 40, 60, 60, 60]

    def draw_static(self):
        self._surface.fill(BACKGROUND)
        self.maze_view.draw_static()
        self.moves_view.draw_static()
        self.draw_buttons()

    def draw_dynamic(self, position: Position):
        self.maze_view.draw_dynamic(position)

    def draw_win(self):
        surface_w, _ = self._surface.get_size()
        text = pygame.font.Font(None, 64).render("Maze Complete!", True, RED, COLOR)
        self._surface.blit(text, ((surface_w - text.get_size()[0]) // 2, 200))

    def draw_buttons(self):
        inside_color_hover = GREEN
        inside_color_normal = BLUE
        color_normal = COLOR
        color_hover = (200, 200, 200)
        symbols = [UP_ARROW, DOWN_ARROW, LEFT_ARROW, RIGHT_ARROW, BACK_SPACE, ENTER, ESC, TIPS, INFO]
        for i in range(9):
            if self.mouse_in_button(i):
                pygame.draw.rect(self._surface, inside_color_hover, pygame.Rect(self.buttons[i][0], self.buttons[i][1], self.button_widths[i], self.button_widths[i]), border_radius = 5)
                self._surface.blit(symbols[i], self.buttons[i])
                pygame.draw.rect(self._surface, color_hover, pygame.Rect(self.buttons[i][0], self.buttons[i][1], self.button_widths[i], self.button_widths[i]), width = 3, border_radius = 5)
            else:
                pygame.draw.rect(self._surface, inside_color_normal, pygame.Rect(self.buttons[i][0], self.buttons[i][1], self.button_widths[i], self.button_widths[i]), border_radius = 5)   
                self._surface.blit(symbols[i], self.buttons[i]) 
                pygame.draw.rect(self._surface, color_normal, pygame.Rect(self.buttons[i][0], self.buttons[i][1], self.button_widths[i], self.button_widths[i]), width = 3, border_radius = 5)
        
    def mouse_in_button(self, i):
        buttons = self.buttons
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] > buttons[i][0] and mouse_pos[0] < buttons[i][0] + self.button_widths[i] and mouse_pos[1] > buttons[i][1] and mouse_pos[1] < buttons[i][1] + self.button_widths[i]:
            return True
        return False

    def tips(self, tip: str):
        text = pygame.font.Font(None, 30).render(tip, True, COLOR, BACKGROUND)
        self._surface.blit(text, (825, 105))
        pygame.draw.rect(self._surface, COLOR, pygame.Rect(820, 100, 350, 100), width=2, border_radius=10)

    def instructions(self):
        text = []
        text.append(pygame.font.Font(None, 30).render(" - Arrow keys or buttons to", True, COLOR, BACKGROUND))
        text.append(pygame.font.Font(None, 30).render("choose directions.", True, COLOR, BACKGROUND))
        text.append(pygame.font.Font(None, 30).render(" - Backspace or button to", True, COLOR, BACKGROUND))
        text.append(pygame.font.Font(None, 30).render("remove them.", True, COLOR, BACKGROUND))
        text.append(pygame.font.Font(None, 30).render(" - Enter or button to make", True, COLOR, BACKGROUND))
        text.append(pygame.font.Font(None, 30).render("the robot cycle.", True, COLOR, BACKGROUND))
        text.append(pygame.font.Font(None, 30).render(" - Escape or button to exit", True, COLOR, BACKGROUND))
        text.append(pygame.font.Font(None, 30).render("to menu.", True, COLOR, BACKGROUND))
        text.append(pygame.font.Font(None, 30).render(" - I or lightbulb button for tips.", True, COLOR, BACKGROUND))
        y = 105
        for sentence in text:
            self._surface.blit(sentence, (825, y))
            y += 30

        
        pygame.draw.rect(self._surface, COLOR, pygame.Rect(820, 100, 350, 300), width=2, border_radius=10)



        


class IAView(View):

    def __init__(self, surface: pygame.Surface, model):
        super().__init__(surface, model)

    def _build(self):
        self.maze_view = MazeView(self._surface, self.model[0].maze)
        self.moves_view = MovesView(self._surface, (self.model[1], self.model[0].no_moves))
        self.results_view = StatsView(self._surface, self.model[2])

    def draw_static(self):
        self._surface.fill(BACKGROUND)
        self.maze_view.draw_static()
        self.moves_view.draw_static()
        self.results_view.draw_static()

    def draw_dynamic(self, position: Position):
        self.maze_view.draw_dynamic(position)