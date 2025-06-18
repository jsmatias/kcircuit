import matplotlib.pyplot as pl

from .shapes.shape import Shape
from .shapes._vector import Vector


class Circuit:

    def __init__(self, config: list[dict[str, object]]):
        self.shapes: list[Shape] = []
        self.config = config

    def build(self):
        prev_item = self.config[0]
        self.shapes.append(prev_item["shape"])
        for item in self.config[1:]:
            prev_shape: Shape = prev_item["shape"]
            out_edge: Vector = prev_shape.edges[prev_item["params"]["connector_out"]]

            shape = item["shape"]
            in_edge = shape.edges[item["params"]["connector_in"]]

            out_connector = prev_shape.connectors[prev_item["params"]["connector_out"]]
            angle_degrees = in_edge.angle_ccw_with(out_edge)

            shape.rotate(180 - angle_degrees)
            in_connector = shape.connectors[item["params"]["connector_in"]]
            shape.shift(out_connector - in_connector)
            self.shapes.append(shape)
            prev_item = item

    def shift(self, distance):
        for s in self.shapes:
            s.shift(distance)

    def plot(self):
        _, ax = pl.subplots(figsize=(7, 7))
        for shape in self.shapes:
            shape.show(ax)
            ax.set_xlim(-10, 20)
            ax.set_ylim(-10, 20)
            ax.grid(ls="--")


