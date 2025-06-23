from collections.abc import Sequence
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from ..shapes.shape import Shape
from ..shapes._vector import Vector


class Circuit:

    def __init__(self, shapes: Sequence[Shape]) -> None:
        self.shapes = shapes

    def build(self):
        prev_shape = self.shapes[0]
        for shape in self.shapes[1:]:
            if shape.in_edge_idx is None or prev_shape.out_edge_idx is None:
                raise Exception(
                    "No connection idx found. "
                    "Make sure to set the `in-` and `out_edge_idx` of the shapes."
                )

            out_edge = prev_shape.edges[prev_shape.out_edge_idx]
            out_connector = prev_shape.connectors[prev_shape.out_edge_idx]
            in_edge = shape.edges[shape.in_edge_idx]

            angle_degrees = in_edge.angle_ccw_with(out_edge)
            shape.rotate(180 - angle_degrees)
            in_connector = shape.connectors[shape.in_edge_idx]
            shape.shift(out_connector - in_connector)
            prev_shape = shape

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

    def plot(self, ax: Axes | None=None) -> Axes:
        ((x_min, y_min), (x_max, y_max)) = self.limit_points()

        min_width = 5
        min_height = 5

        width = x_max - x_min
        height = y_max - y_min

        if width < min_width:
            center_x = (x_min + x_max) / 2
            x_min = center_x - min_width / 2
            x_max = center_x + min_width / 2
            width = min_width

        if height < min_height:
            center_y = (y_min + y_max) / 2
            y_min = center_y - min_height / 2
            y_max = center_y + min_height / 2
            height = min_height

        padding = 0.1
        x_lims = (x_min - padding * width, x_max + padding * width)
        y_lims = (y_min - padding * height, y_max + padding * height)

        if ax is None:
            _, ax = plt.subplots()

        ax.set_aspect("equal")

        for shape in self.shapes:
            shape.plot(ax)

        ax.set_xlim(*x_lims)
        ax.set_ylim(*y_lims)
        ax.grid(ls="--")
        plt.tight_layout()
        return ax
        