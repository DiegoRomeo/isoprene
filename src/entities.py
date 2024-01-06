from abc import ABC
from math import acos
from vmath import Vector3D, scalar_multiplication

class Entity(ABC):

    def update(self, dt: float):
        pass


class Atom(Entity):

    def __init__(self, mass, interaction_radius, interaction_strength, position: Vector3D, image, charge=0.0, velocity=Vector3D(0, 0, 0), acceleration=Vector3D(0, 0, 0), force=Vector3D(0, 0, 0)) -> None:
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.force = force

        self.mass = mass
        self.charge = charge

        self.interaction_radius = interaction_radius
        self.interaction_strength = interaction_strength

        self.image = image

    def update(self, dt):
        self.acceleration = self.force / self.mass

        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

        
        # Reset total force
        self.force.x, self.force.y, self.force.z = 0, 0, 0


class Bond:

    def __init__(self, atom, other, potential_strength, natural_length) -> None:
        self.atom = atom
        self.other = other
        self.potential_strength = potential_strength
        self.natural_length = natural_length

    @property
    def length(self):
        return (self.atom.position - self.other.position).norm()


class Angle:

    def __init__(self, atom1, atom2, atom3, bending_force_constant, natural_angle) -> None:
        self.atom1 = atom1
        self.atom2 = atom2
        self.atom3 = atom3
        self.bending_force_constant = bending_force_constant
        self.natural_angle = natural_angle

    @property
    def actual_angle(self):
        distance1 = self.atom1.position - self.atom2.position
        distance2 = self.atom3.position - self.atom2.position

        scalar_product = scalar_multiplication(distance1, distance2)
        product_of_norms = distance1.norm() * distance2.norm()

        angle = acos(scalar_product / product_of_norms)
        return angle

class Molecule:

    def __init__(self, bonds: list[Bond], angles: list[Angle]) -> None:
        self.bonds = bonds
        self.angles = angles

        self.atoms = []
        for bond in self.bonds:
            if bond.atom not in self.atoms:
                self.atoms.append(bond.atom)
            if bond.other not in self.atoms:
                self.atoms.append(bond.other)
