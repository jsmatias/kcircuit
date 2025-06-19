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
        self.contour_vectors = self._build_contour_vectors()


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

    def _build_contour_vectors(self, n_points: int=1) -> list[Vector]:

        internal_r0 = self.vectors[0] - self.centre
        internal_r1 = self.vectors[3] - self.centre
        external_r0 = self.vectors[1] - self.centre

        start_angle = internal_r0.angle_ccw_with(Vector(1, 0)) 
        end_angle = internal_r1.angle_ccw_with(Vector(1, 0)) 
        angle_range = np.linspace(start_angle, end_angle, int(end_angle - start_angle) * n_points)

        contour_vectors: list[Vector] = []
        for angle in angle_range:
            angle_rad = math.radians(angle)
            ex_x = external_r0.magnitude() * math.cos(angle_rad) + self.centre.x
            ex_y = external_r0.magnitude() * math.sin(angle_rad) + self.centre.y
            contour_vectors.append(Vector(ex_x, ex_y))

        for angle in angle_range[::-1]:
            angle_rad = math.radians(angle)
            in_x = internal_r0.magnitude() * math.cos(angle_rad) + self.centre.x
            in_y = internal_r0.magnitude() * math.sin(angle_rad) + self.centre.y
            contour_vectors.append(Vector(in_x, in_y))
        
        # contour_vectors.append(contour_vectors[-1])
        return contour_vectors
        

        # # Get the correct counterclockwise angles
        # start_angle = math.atan2(an_internal_r.y, an_internal_r.x)
        # end_angle = math.atan2(another_internal_r.y, another_internal_r.x)

        # # Ensure counterclockwise order
        # if end_angle < start_angle:
        #     end_angle += 2 * math.pi



        # self.contour = (
        #     [self.vectors[0].x]
        #     + [
        #         an_external_r.magnitude() * math.cos(angle_i) + self.centre.x
        #         for angle_i in angle_range
        #     ]
        #     + [self.vectors[2].x]
        #     + [
        #         an_internal_r.magnitude() * math.cos(angle_i) + self.centre.x
        #         for angle_i in angle_range[::-1]
        #     ],
        #     [self.vectors[0].y]
        #     + [
        #         an_external_r.magnitude() * math.sin(angle_i) + self.centre.y
        #         for angle_i in angle_range
        #     ]
        #     + [self.vectors[2].y]
        #     + [
        #         an_internal_r.magnitude() * math.sin(angle_i) + self.centre.y
        #         for angle_i in angle_range[::-1]
        #     ],
        # )
