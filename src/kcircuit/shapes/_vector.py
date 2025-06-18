import math

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: "Vector"):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector"):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: int | float):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: int | float):
        return self.__mul__(scalar)

    def __imul__(self, scalar: int | float):
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float | int) -> "Vector":
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return Vector(self.x / scalar, self.y / scalar)
    
    def __repr__(self) -> str:
        return f"Vector({self.x},{self.y})"

    def dot(self, other: "Vector"):
        return self.x * other.x + self.y * other.y

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def rotate(self, angle_degrees: float):
        angle_radians = math.radians(angle_degrees)
        cos_a, sin_a = math.cos(angle_radians), math.sin(angle_radians)
        x_new = self.x * cos_a - self.y * sin_a
        y_new = self.x * sin_a + self.y * cos_a
        return Vector(x_new, y_new)

    def angle_with(self, other: "Vector"):
        """Returns the angle (in degrees) between this vector and another."""
        dot_product = self.dot(other)
        magnitudes = self.magnitude() * other.magnitude()
        if magnitudes == 0:
            raise ValueError("Cannot compute angle with a zero vector")
        cos_theta = dot_product / magnitudes
        cos_theta = max(-1, min(1, cos_theta))  # Clamp to avoid precision errors
        return math.degrees(math.acos(cos_theta))

    def angle_ccw_with(self, other: "Vector"):
        """Returns the counterclockwise angle (in degrees) from 'other' to 'self'."""
        angle1 = math.atan2(self.y, self.x)
        angle2 = math.atan2(other.y, other.x)
        angle = math.degrees(angle1 - angle2)

        # Ensure the angle is always in [0, 360)
        return angle + 360 if angle < 0 else angle
