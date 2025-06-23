from ._vector import Vector
from ._polygon import Polygon


class Rectangle(Polygon):

    def __init__(self, width: float, length: float,):
        self.width = width
        self.length = length
        super().__init__()

    def build_vectors(self):

        for sign in [(1, 1), (-1, 1), (-1, -1), (1, -1)]:
            vertix = Vector(sign[0] * self.length / 2, sign[1] * self.width / 2)
            self.vectors.append(vertix)
            self.contour_vectors.append(vertix)
