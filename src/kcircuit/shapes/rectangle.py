from ._vector import Vector
from ._polygon import Polygon


class Rectangle(Polygon):

    def build_vectors(
        self,
        width: float,
        length: float,
        *args,
        **kwargs,
    ):
        self.width = width
        self.length = length

        for sign in [(1, 1), (-1, 1), (-1, -1), (1, -1)]:
            self.vectors.append(
                Vector(sign[0] * self.length / 2, sign[1] * self.width / 2)
            )
