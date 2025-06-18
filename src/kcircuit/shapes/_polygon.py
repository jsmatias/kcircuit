from abc import ABC, abstractmethod

from .shape import Shape


class Polygon(Shape, ABC):

    @abstractmethod
    def build_vectors(self, *args, **kwargs) -> None:
        pass

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

    def _build_contour(self):
        self.contour = (
            [v.x for v in self.vectors + [self.vectors[0]]],
            [v.y for v in self.vectors + [self.vectors[0]]],
        )