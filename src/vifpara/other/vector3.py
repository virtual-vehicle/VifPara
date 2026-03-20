# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:et

from math import sqrt
from typing import Union



class Vector3:
    def __init__(self, x: Union[float, int], y: Union[float, int], z: Union[float, int]) -> None:
        """
        Initialize a 3-dimensional vector.

        :param float|int x: The x-component of the vector.
        :param float|int y: The y-component of the vector.
        :param float|int z: The z-component of the vector.
        :return: None
        """
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    @classmethod
    def from_list(cls, vector):
        """
        Create a ``Vector3`` instance from a list of numerical values.

        :param list[float|int] vector: A list containing three numeric components ``[x, y, z]``.
        :return Vector3: A new ``Vector3`` constructed from the list values.
        """
        return cls(x=vector[0], y=vector[1], z=vector[2])

    @classmethod
    def right(cls):
        """
        Create a right-direction unit vector ``(1.0, 0.0, 0.0)``.

        :return Vector3: A unit vector pointing in the positive X direction.
        """
        return cls(1.0, 0.0, 0.0)

    @classmethod
    def up(cls):
        """
        Create an up-direction unit vector ``(0.0, 1.0, 0.0)``.

        :return Vector3: A unit vector pointing in the positive Y direction.
        """
        return cls(0.0, 1.0, 0.0)

    @classmethod
    def forward(cls):
        """
        Create a forward-direction unit vector ``(0.0, 0.0, 1.0)``.

        :return Vector3: A unit vector pointing in the positive Z direction.
        """
        return cls(0.0, 0.0, 1.0)

    @classmethod
    def zero(cls):
        """
        Create a zero vector ``(0.0, 0.0, 0.0)``.

        :return Vector3: A vector with all components set to zero.
        """
        return cls(0.0, 0.0, 0.0)

    @classmethod
    def one(cls):
        """
        Create a ones vector ``(1.0, 1.0, 1.0)``.

        :return Vector3: A vector with all components set to one.
        """
        return cls(1.0, 1.0, 1.0)

    def set(self, x: int, y: int, z: int) -> None:
        """
        Set all three components of the vector.

        :param int x: The new x-component value.
        :param int y: The new y-component value.
        :param int z: The new z-component value.
        :return: None
        """
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, rhs):
        if isinstance(rhs, Vector3):
            return Vector3(self.x+rhs.x, self.y+rhs.y, self.z+rhs.z)

        raise TypeError

    def __sub__(self, rhs):
        if isinstance(rhs, Vector3):
            return Vector3(self.x-rhs.x, self.y-rhs.y, self.z-rhs.z)

        if isinstance(rhs, (int, float)):
            return Vector3(self.x-rhs, self.y-rhs, self.z-rhs)

        raise TypeError

    def __mul__(self, rhs):
        if isinstance(rhs, Vector3):
            return Vector3(self.x*rhs.x, self.y*rhs.y, self.z*rhs.z)

        if isinstance(rhs, (int, float)):
            return Vector3(self.x*rhs, self.y*rhs, self.z*rhs)

        raise TypeError

    def __truediv__(self, rhs):
        if isinstance(rhs, float):
            return Vector3(self.x/rhs, self.y/rhs, self.z/rhs)

        raise ValueError

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def dot(self, rhs):
        """
        Compute the dot product between this vector and another.

        :param Vector3 rhs: The vector to compute the dot product with.
        :return float|int: The resulting dot product value.
        :raises TypeError: If ``rhs`` is not a ``Vector3``.
        """
        if isinstance(rhs, Vector3):
            return self.x * rhs.x + self.y * rhs.y + self.z * rhs.z

        raise TypeError

    def cross(self, rhs):
        """
        Compute the cross product between this vector and another.

        :param Vector3 rhs: The vector to compute the cross product with.
        :return Vector3: A new vector representing the cross product result.
        :raises TypeError: If ``rhs`` is not a ``Vector3``.
        """
        if isinstance(rhs, Vector3):
            return Vector3(self.y * rhs.z - self.z * rhs.y,
                        -self.x * rhs.z + self.z * rhs.x,
                        self.x * rhs.y - self.y * rhs.x)

        raise TypeError

    def magnitude(self):
        """
        Compute the magnitude (Euclidean length) of the vector.

        :return float: The computed vector magnitude.
        """
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalized(self):
        """
        Return a normalized (unit‑length) version of this vector.

        If the vector has zero magnitude, the result is ``Vector3(0, 0, 0)``.

        :return Vector3: The normalized vector.
        """
        mag = self.magnitude()

        if mag > 0.0:
            fac = 1.0 / mag
        else:
            fac = 0.0

        return self * fac

    def __getitem__(self, key):

        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z

        raise IndexError

    def __repr__(self):
        return 'Vec(%g, %g, %g)' % (self.x, self.y, self.z)

    def __str__(self):
        return '(%g, %g, %g)' % (self.x, self.y, self.z)

    def to_list(self):
        """
        Convert the vector into a Python list.

        :return list[int|float]: A list containing ``[x, y, z]``.
        """
        return [self.x, self.y, self.z]



