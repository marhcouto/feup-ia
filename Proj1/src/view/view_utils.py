from view.view_const import COLOR, GREY

class MazeEdge:

    def __init__(self, width, color):
        self.__width = width
        self.__color = color

    @property
    def width(self):
        return self.__width

    @property
    def color(self):
        return self.__color


class EdgeFactory:
    @staticmethod
    def real_wall():
        return MazeEdge(4, COLOR)

    @staticmethod
    def no_wall():
        return MazeEdge(1, GREY)
