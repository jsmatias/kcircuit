from abc import ABC, abstractmethod

import matplotlib.pyplot as pl
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
        self.vectors = []
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

    @abstractmethod
    def _build_contour(self) -> None:
        pass

    def to_klayout(self, unit:str = "nm") -> kdb.Polygon:
        """Convert to int considering units!"""
        points = [kdb.Point(int(x), int(y)) for x, y in zip(self.contour[0], self.contour[1])]
        return kdb.Polygon(points)

    def shift(self, shift_vector: Vector) -> None:
        self.vectors = [v + shift_vector for v in self.vectors]
        self.centre += shift_vector
        self._build_edges()
        self._build_connectors()
        self._build_contour()

    def rotate(self, angle_degrees: float) -> None:
        for i, v in enumerate(self.vectors):
            rotated_v = (v - self.centre).rotate(angle_degrees) + self.centre
            self.vectors[i] = rotated_v
        self._build_edges()
        self._build_connectors()
        self._build_contour()

    def show(self, ax: Axes | None=None, show_indices: bool=False) -> Axes:
        pl.ion()
        if ax is None:
            _, ax = pl.subplots(figsize=(7, 7))
        x = self.contour[0]
        y = self.contour[1]
        ax.plot(x, y, color="orangered")

        x1 = [c.x for c in self.connectors]
        y1 = [c.y for c in self.connectors]
        ax.plot(self.centre.x, self.centre.y, "+", color="gray")
        ax.plot(x1, y1, "o", ms=3, color="gray")

        if show_indices:
            for i, connector in enumerate(self.connectors):
                ax.text(connector.x, connector.y, str(i), fontsize=10, ha="right")

        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        pl.tight_layout()
        return ax
