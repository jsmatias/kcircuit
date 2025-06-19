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

    def __init__(self, *args, **kwargs):
        self.vectors: list[Vector] = []
        self.contour_vectors: list[Vector] = []
        self.edges = []
        self.connectors = []
        self.contour = ([], [])
        self.centre = Vector(0, 0)
        self.build_vectors(*args, **kwargs)
        self._build_edges()
        self._build_connectors()
        self._build_contour()

    @abstractmethod
    def build_vectors(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def _build_edges(self) -> None:
        pass

    @abstractmethod
    def _build_connectors(self) -> None:
        pass

    def _build_contour(self):
        self.contour = (
            [v.x for v in self.contour_vectors + [self.contour_vectors[0]]],
            [v.y for v in self.contour_vectors + [self.contour_vectors[0]]],
        )

    def to_klayout(self, unit:str = "nm") -> kdb.Polygon:
        """Convert to int considering units!"""
        points = [kdb.Point(int(x), int(y)) for x, y in zip(self.contour[0], self.contour[1])]
        return kdb.Polygon(points)

    def shift(self, shift_vector: Vector) -> None:
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
            if "x" in axis:
                v.y = -v.y
            if "y" in axis:
                v.x = -v.x

        for v in self.contour_vectors:
            if "x" in axis:
                v.y = -v.y
            if "y" in axis:
                v.x = -v.x
        
        self._build_edges()
        self._build_connectors()
        self._build_contour()

    def mirror(self, x_axis_pos: float | None=None, y_axis_pos: float | None=None) -> None:
        
        if y_axis_pos is not None:
            self.shift(Vector(-y_axis_pos, 0))
            self.flip(axis="y")
            self.shift(Vector(y_axis_pos, 0))
        
        if x_axis_pos is not None:
            self.shift(Vector(-x_axis_pos, 0))
            self.flip(axis="x")
            self.shift(Vector(x_axis_pos, 0))


    def limit_points(self) -> tuple[tuple[float, float], tuple[float, float]]:
        x_min = min(self.contour[0]) 
        x_max = max(self.contour[0]) 
        y_min = min(self.contour[1]) 
        y_max = max(self.contour[1]) 

        return (x_min, y_min), (x_max, y_max)


    def plot(self, ax: Axes | None = None, show_indices: bool = False) -> Axes:
        plt.ion()
        if ax is None:
            _, ax = plt.subplots(figsize=(7, 7))

        x, y = self.contour
        ax.plot(x, y, color="orangered")

        x1 = [c.x for c in self.connectors]
        y1 = [c.y for c in self.connectors]
        ax.plot(self.centre.x, self.centre.y, "+", color="gray")
        ax.plot(x1, y1, "o", ms=3, color="gray")

        if show_indices:
            for i, connector in enumerate(self.connectors):
                ax.text(connector.x, connector.y, str(i), fontsize=10, ha="right")

        (x_min, y_min), (x_max, y_max) = self.limit_points()

        min_size = 1.0
        width = max(x_max - x_min, min_size)
        height = max(y_max - y_min, min_size)

        cx = (x_min + x_max) / 2
        cy = (y_min + y_max) / 2
        x_min, x_max = cx - width / 2, cx + width / 2
        y_min, y_max = cy - height / 2, cy + height / 2

        padding = 0.1
        ax.set_xlim(x_min - padding * width, x_max + padding * width)
        ax.set_ylim(y_min - padding * height, y_max + padding * height)
        ax.set_aspect("equal")
        ax.grid(ls="--")
        plt.tight_layout()

        return ax
