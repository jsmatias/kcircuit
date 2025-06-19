import numpy as np

from ._vector import Vector
from ._polygon import Polygon

class Taper(Polygon):
    """
    A taper structure has a varying width proportional to a tarper function with an coefficient `m`.
    For `m=1` the function becames linear and the taper is reduced to a trapezoid. 
    ```
    |''---....__
    |           |
    |           |
    |__...----''
    ```
    """

    def build_vectors(
        self, 
        wide_width: float, 
        narrow_width: float, 
        length: float, 
        taper_exponent: float = 1, 
        *args, **kwargs # type: ignore
    ) -> None:
        
        self.narrow_width = narrow_width
        self.wide_width = wide_width
        self.length = length
        self.taper_exponent = taper_exponent

        self.vectors.append(Vector(+ self.length / 2, + self.narrow_width / 2))
        self.vectors.append(Vector(- self.length / 2, + self.wide_width / 2))
        self.vectors.append(Vector(- self.length / 2, - self.wide_width / 2))
        self.vectors.append(Vector(+ self.length / 2, - self.narrow_width / 2))

        self.contour_vectors = self._build_contour_vectors()

    def _taper_width(self, x: float) -> float:
        """
        This is centred in x=0.
        x' -> x + l/2
        """
        w1 = self.wide_width
        w2 = self.narrow_width
        l = self.length
        m = self.taper_exponent

        alpha = (w1 - w2) / l ** m
        return alpha * (l / 2 - x) ** m + w2

    def _build_contour_vectors(self, n_points: int=10) -> list[Vector]:

        x_arr = list(np.linspace(-self.length / 2, self.length / 2, n_points)[::-1])
        y_arr = [self._taper_width(x) / 2 for x in x_arr]
        
        x_arr = x_arr + x_arr[::-1]
        y_arr = y_arr + [-y for y in y_arr[::-1]]

        contour_vectors: list[Vector] = []
        for x, y in zip(x_arr, y_arr):
            contour_vectors.append(Vector(x, y))

        return contour_vectors


