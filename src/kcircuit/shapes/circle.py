import math
import numpy as np

from ._vector import Vector
from .shape import Shape


class Circular(Shape):

    def build_vectors(
        self, width: float, radius: float, angle_degrees: float, *args, **kwargs
    ) -> None:
        angle_radians = math.radians(angle_degrees)

        internal_r = radius - width / 2
        external_r = radius + width / 2

        self.vectors = [
            Vector(internal_r, 0),
            Vector(external_r, 0),
            Vector(
                external_r * math.cos(angle_radians),
                external_r * math.sin(angle_radians),
            ),
            Vector(
                internal_r * math.cos(angle_radians),
                internal_r * math.sin(angle_radians),
            ),
        ]

    def _build_edges(self) -> None:
        self.edges = [
            self.vectors[1] - self.vectors[0],
            self.vectors[3] - self.vectors[2],
        ]

    def _build_connectors(self) -> None:
        self.connectors = [
            (self.vectors[0] + self.vectors[(1) % len(self.vectors)]) / 2,
            (self.vectors[2] + self.vectors[(3) % len(self.vectors)]) / 2,
        ]

    def _build_contour(self):

        # Vectors relative to the center
        an_internal_r = self.vectors[0] - self.centre
        another_internal_r = self.vectors[3] - self.centre
        an_external_r = self.vectors[1] - self.centre

        # Get the correct counterclockwise angles
        start_angle = math.atan2(an_internal_r.y, an_internal_r.x)
        end_angle = math.atan2(another_internal_r.y, another_internal_r.x)

        # Ensure counterclockwise order
        if end_angle < start_angle:
            end_angle += 2 * math.pi

        angle_range = np.arange(start_angle, end_angle, 0.01)

        # an_internal_r = self.vectors[0] - self.centre
        # another_internal_r = self.vectors[3] - self.centre
        # an_external_r = self.vectors[1] - self.centre

        # start_angle = an_internal_r.angle_with(Vector(1, 0))
        # end_angle = another_internal_r.angle_with(Vector(1, 0))
        # start_angle_radians = math.radians(
        #     360 - start_angle if an_internal_r.y < 0 else start_angle
        # )
        # end_angle_radians = math.radians(
        #     360 - end_angle if another_internal_r.y < 0 else end_angle
        # )
        # angle_range = np.arange(start_angle_radians, end_angle_radians, 0.01)

        self.contour = (
            [self.vectors[0].x]
            + [
                an_external_r.magnitude() * math.cos(angle_i) + self.centre.x
                for angle_i in angle_range
            ]
            + [self.vectors[2].x]
            + [
                an_internal_r.magnitude() * math.cos(angle_i) + self.centre.x
                for angle_i in angle_range[::-1]
            ],
            [self.vectors[0].y]
            + [
                an_external_r.magnitude() * math.sin(angle_i) + self.centre.y
                for angle_i in angle_range
            ]
            + [self.vectors[2].y]
            + [
                an_internal_r.magnitude() * math.sin(angle_i) + self.centre.y
                for angle_i in angle_range[::-1]
            ],
        )
