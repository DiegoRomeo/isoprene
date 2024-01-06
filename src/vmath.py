from __future__ import annotations

from math import sqrt

class Vector3D:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, vector: Vector3D) -> Vector3D:
        return Vector3D(self.x + vector.x, 
                        self.y + vector.y, 
                        self.z + vector.z)

    def __sub__(self, vector: Vector3D) -> Vector3D:
        return Vector3D(self.x - vector.x,
                        self.y - vector.y, 
                        self.z - vector.z)

    def __mul__(self, other=None) -> Vector3D:
        if isinstance(other, int) or isinstance(other, float):
            return Vector3D(self.x * other,
                            self.y * other,
                            self.z * other)
        
        elif isinstance(other, Vector3D):
            return Vector3D(self.x * other.x,
                            self.y * other.y,
                            self.z * other.z)

        else:
            raise(TypeError)

    def __truediv__(self, other=None) -> Vector3D:
        if isinstance(other, int) or isinstance(other, float):
            return Vector3D(self.x / other,
                            self.y / other,
                            self.z / other)
        
        elif isinstance(other, Vector3D):
            return Vector3D(self.x / other.x,
                            self.y / other.y,
                            self.z / other.z)

        else:
            raise(TypeError)


    def __pow__(self, n=None) -> Vector3D:

        if isinstance(n, int) or isinstance(n, float):
            return Vector3D(self.x**n,
                            self.y**n,
                            self.z**n)
        else:
            raise(TypeError)

    def __str__(self) -> str:
        return str({"x": self.x, "y": self.y, "z": self.z})

    def __repr__(self) -> str:
        return str({"x": self.x, "y": self.y, "z": self.z})


    def norm(self) -> float:
        return sqrt(self.x**2 + self.y**2 + self.z**2)

def scalar_multiplication(vector1: Vector3D, vector2: Vector3D):
    return vector1.x * vector2.x + vector1.y * vector2.y + vector1.z * vector2.z

def isometric(coordinates: Vector3D) -> tuple[float, float]:
    x = -coordinates.x + coordinates.y
    y = -(coordinates.x + coordinates.y) / 2 + coordinates.z

    return x, y
