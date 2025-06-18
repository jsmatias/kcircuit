import matplotlib.pyplot as pl

from ..shapes.shape import Shape
from ..shapes._vector import Vector


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

    def shift(self, shift_vector: Vector):
        for s in self.shapes:
            s.shift(shift_vector)

    def centre(self) -> Vector:
        (x_min, y_min), (x_max, y_max) = self.limit_points()
        x_centre = (x_max + x_min) / 2
        y_centre = (y_max + y_min) / 2
        return Vector(x_centre, y_centre)

    def centralize(self) -> None:
        self.shift(-1 * self.centre())

    def limit_points(self) -> tuple[tuple[float, float], tuple[float, float]]:

        x_min, x_max, y_min, y_max = None, None, None, None
        for shape in self.shapes:
            ((shape_x_min, shape_y_min), (shape_x_max, shape_y_max)) = shape.limit_points()
            x_min = min(x_min, shape_x_min) if x_min else shape_x_min
            y_min = min(y_min, shape_y_min) if y_min else shape_y_min
            x_max = max(x_max, shape_x_max) if x_max else shape_x_max
            y_max = max(y_max, shape_y_max) if y_max else shape_y_max
        
        if x_min is None or y_min is None or x_max is None or y_max is None:
            raise ValueError("At least one of the limit points of this circuit is a None value.")

        return (x_min, y_min), (x_max, y_max)


    def plot(self):

        ((x_min, y_min), (x_max, y_max)) = self.limit_points()

        height = y_max - y_min
        width = x_max - x_min
        ratio = height / width
        padding = 0.1

        x_lims = ((1 + padding) * x_min, (1 + padding) * x_max)
        y_lims = ((1 + padding) * y_min, (1 + padding) * y_max)
        print(*x_lims)
        print(*y_lims)
        _, ax = pl.subplots(figsize=(7 / ratio, 7))
        for shape in self.shapes:
            shape.show(ax)
            ax.set_xlim(*x_lims)
            ax.set_ylim(*y_lims)
            ax.grid(ls="--")


