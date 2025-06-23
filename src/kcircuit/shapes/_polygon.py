from abc import ABC

from .shape import Shape


class Polygon(Shape, ABC):

    # TODO: Def build_contour_vectors

    def _build_edges(self) -> None:
        self.edges = [
            self.vectors[(i + 1) % len(self.vectors)] - self.vectors[i]
            for i in range(len(self.vectors))
        ]
        
    def _build_connectors(self) -> None:
        self.connectors = [
            (self.vectors[i] + self.vectors[(i + 1) % len(self.vectors)]) / 2
            for i in range(len(self.vectors))
        ]