from copy import deepcopy
from collections.abc import Sequence

import klayout.db as kdb
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

    def mirror(self, x_axis_pos: float | None=None, y_axis_pos: float | None=None) -> None:
        for shape in self.shapes:
            shape.mirror(x_axis_pos, y_axis_pos)

    def copy(self) -> "Circuit":
        return deepcopy(self)

    def limit_points(self) -> tuple[tuple[float, float], tuple[float, float]]:

        x_min, x_max, y_min, y_max = None, None, None, None
        for shape in self.shapes:
            ((shape_x_min, shape_y_min), (shape_x_max, shape_y_max)) = shape.limit_points()
            x_min = min(x_min, shape_x_min) if x_min is not None else shape_x_min
            y_min = min(y_min, shape_y_min) if y_min is not None else shape_y_min
            x_max = max(x_max, shape_x_max) if x_max is not None else shape_x_max
            y_max = max(y_max, shape_y_max) if y_max is not None else shape_y_max
        
        if x_min is None or y_min is None or x_max is None or y_max is None:
            raise ValueError("At least one of the limit points of this circuit is a None value.")

        return (x_min, y_min), (x_max, y_max)
    
    def to_klayout(self) -> list[kdb.Polygon]:
        """Export all shapes in the circuit to a list of Klayout Polygons.
        """
        return [shape.to_klayout() for shape in self.shapes]

    def plot(self, ax: Axes | None=None) -> Axes:
        
        if ax is None:
            _, ax = plt.subplots()

        ax.set_aspect("equal")

        for shape in self.shapes:
            shape.plot(ax)

        ax.grid(ls="--")
        return ax
        