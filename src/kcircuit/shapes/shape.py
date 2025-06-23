from copy import deepcopy
from abc import ABC, abstractmethod
from typing import Literal

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import klayout.db as kdb

from ._vector import Vector


class Shape(ABC):
    vectors: list[Vector]
    edges: list[Vector]
    connectors: list[Vector]
    centre: Vector
    contour: tuple[list[float], list[float]]

    def __init__(self):
        self.vectors: list[Vector] = []
        self.contour_vectors: list[Vector] = []
        self.edges = []
        self.connectors = []
        self.contour = ([], [])
        self.centre = Vector(0, 0)
        self.in_edge_idx: int | None = None 
        self.out_edge_idx: int | None = None
        self.build_vectors()
        self._build_edges()
        self._build_connectors()
        self._build_contour()

    @abstractmethod
    def build_vectors(self) -> None:
        pass

    @abstractmethod
    def _build_edges(self) -> None:
        pass

    @abstractmethod
    def _build_connectors(self) -> None:
        pass

    def set_connectors(self, in_edge_idx: int | None = None, out_edge_idx: int | None = None):

        if in_edge_idx and in_edge_idx > len(self.edges) or out_edge_idx and out_edge_idx > len(self.edges):
            raise Exception("Index should not be greater than the number of the shape's edges.")
        
        self.in_edge_idx = in_edge_idx
        self.out_edge_idx = out_edge_idx
        return self

    def _build_contour(self):
        self.contour = (
            [v.x for v in self.contour_vectors + [self.contour_vectors[0]]],
            [v.y for v in self.contour_vectors + [self.contour_vectors[0]]],
        )

    def to_klayout(self, unit:Literal["mm", "um", "nm"] = "nm") -> kdb.Polygon:
        """Export to Klayout Polygon.
        All values are converted to nm.
        """
        if unit not in ("mm", "um", "nm"):
            raise Exception("Please especify a valid unit: 'nm', 'um' or 'mm'.")
        
        points: list[kdb.Point] = []
        for x, y in zip(self.contour[0], self.contour[1]):
            factor = 1
            if unit=="um":
                factor = 1000 
            if unit=="mm": 
                factor = 1000000

            points.append(kdb.Point(round(factor * x), round(factor * y)))

        return kdb.Polygon(points)

    def shift(self, delta_x: float, delta_y: float) -> None:
        shift_vector = Vector(delta_x, delta_y)
        self.vectors = [v + shift_vector for v in self.vectors]
        self.contour_vectors = [v + shift_vector for v in self.contour_vectors]

        self.centre += shift_vector
        self._build_edges()
        self._build_connectors()
        self._build_contour()

    def rotate(self, angle_degrees: float) -> None:
        for i, v in enumerate(self.vectors):
            rotated_v = (v - self.centre).rotate(angle_degrees) + self.centre
            self.vectors[i] = rotated_v

        for i, v in enumerate(self.contour_vectors):
            rotated_v = (v - self.centre).rotate(angle_degrees) + self.centre
            self.contour_vectors[i] = rotated_v
        self._build_edges()
        self._build_connectors()
        self._build_contour()

    def flip(self, axis: Literal["x", "y", "xy"]) -> None:
        for v in self.vectors:
            if "x" in axis: v.y = -v.y
            if "y" in axis: v.x = -v.x

        for v in self.contour_vectors:
            if "x" in axis: v.y = -v.y
            if "y" in axis: v.x = -v.x

        if "x" in axis: self.centre.y *= -1
        if "y" in axis: self.centre.x *= -1 
        
        self._build_edges()
        self._build_connectors()
        self._build_contour()

    def mirror(self, x_axis_pos: float | None=None, y_axis_pos: float | None=None) -> None:
        
        if y_axis_pos is not None:
            self.shift(-y_axis_pos, 0)
            self.flip(axis="y")
            self.shift(y_axis_pos, 0)
        
        if x_axis_pos is not None:
            self.shift(0, -x_axis_pos)
            self.flip(axis="x")
            self.shift(0, x_axis_pos)

    def copy(self) -> "Shape":
        return deepcopy(self)

    def limit_points(self) -> tuple[tuple[float, float], tuple[float, float]]:
        x_min = min(self.contour[0]) 
        x_max = max(self.contour[0]) 
        y_min = min(self.contour[1]) 
        y_max = max(self.contour[1]) 

        return (x_min, y_min), (x_max, y_max)


    def plot(self, ax: Axes | None=None, show_indices: bool=False, allow_stretch:bool=False) -> Axes:
        if ax is None:
            _, ax = plt.subplots(figsize=(10, 7))
            ax.set_aspect("auto" if allow_stretch else "equal", "datalim")
            ax.grid(ls="--")

        x, y = self.contour
        ax.plot(x, y, color="orangered")

        x1 = [c.x for c in self.connectors]
        y1 = [c.y for c in self.connectors]
        ax.plot(self.centre.x, self.centre.y, "+", color="gray")
        ax.plot(x1, y1, "o", ms=3, color="gray")

        if show_indices:
            for i, connector in enumerate(self.connectors):
                ax.text(connector.x, connector.y, str(i), fontsize=10, ha="right")
        fig = ax.get_figure()
        fig.tight_layout()

        return ax
