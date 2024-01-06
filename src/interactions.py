from math import cos, degrees, sin, acos, sqrt
from vmath import Vector3D, scalar_multiplication
from entities import Atom

class Interaction:

    def __init__(self, force, *force_args) -> None:
        self.force = force
        self.force_args = force_args

    def update_forces(self):
        self.force(*self.force_args)



class InteractionRegistry:

    def __init__(self) -> None:
        self._interactions = []

    @property
    def interactions(self):
        return self._interactions

    @interactions.setter
    def interactions(self, _interactions: list[Interaction]):
        self._interactions = _interactions

    def add_interaction(self, interaction: Interaction):
        if interaction not in self._interactions:
            self._interactions.append(interaction)

    def remove_interaction(self, interaction):
        # Does not delete the Interaction object (because it may be re-added in future)
        # This feature could be used for optimization (removing interactions when they are trascurable and re-adding them when they are not)
        self._interactions.remove(interaction)

    def update_interactions(self):
        for interaction in self._interactions:
            interaction.update_forces()


def lennard_jones(atom1: Atom, atom2: Atom, sigma: float, epsilon: float):
    distance_vector = atom1.position - atom2.position
    r = distance_vector.norm()

    if round(r) == 0 or r > 14:
        return Vector3D(0, 0, 0)
    
    direction = distance_vector / r
    force = direction * -24 * epsilon * ((sigma / r)**6 - 2 * (sigma / r)**12) / r

    atom1.force += force
    atom2.force -= force


def bond_stretching(atom1: Atom, atom2: Atom, stretching_force_constant: float, natural_bond_length: float):
    distance = atom1.position - atom2.position
    actual_bond_length = distance.norm()
    direction = distance / actual_bond_length
    
    force = direction * -2 * stretching_force_constant * (actual_bond_length - natural_bond_length)
    
    atom1.force += force
    atom2.force -= force

def angle_bending(atom1: Atom, atom2: Atom, atom3: Atom, bending_force_constant: float, natural_bond_angle):
    distance1 = atom1.position - atom2.position
    distance2 = atom3.position - atom2.position

    scalar_product = scalar_multiplication(distance1, distance2)
    product_of_norms = distance1.norm() * distance2.norm()
    
    actual_bond_angle = acos(scalar_product / product_of_norms)

    denominator = sqrt(1.0 - cos(actual_bond_angle)**2)

    numerator1_x = (distance2.x - scalar_product/(2*distance1.norm()**2)) / product_of_norms
    numerator1_y = (distance2.y - scalar_product/(2*distance1.norm()**2)) / product_of_norms
    numerator1_z = (distance2.z - scalar_product/(2*distance1.norm()**2)) / product_of_norms

    numerator3_x = (distance1.x - scalar_product/(2*distance2.norm()**2)) / product_of_norms
    numerator3_y = (distance1.y - scalar_product/(2*distance2.norm()**2)) / product_of_norms
    numerator3_z = (distance1.z - scalar_product/(2*distance2.norm()**2)) / product_of_norms


    numerator2_x = (distance1.x *-1 - distance2.x - scalar_product*(distance1.x/distance1.norm()**2 - distance2.x/distance2.norm()**2)) / product_of_norms
    numerator2_y = (distance1.y *-1 - distance2.y - scalar_product*(distance1.y/distance1.norm()**2 - distance2.y/distance2.norm()**2)) / product_of_norms
    numerator2_z = (distance1.z *-1 - distance2.z - scalar_product*(distance1.z/distance1.norm()**2 - distance2.z/distance2.norm()**2)) / product_of_norms

    force1_x = 2 * bending_force_constant * (actual_bond_angle - natural_bond_angle) / denominator * numerator1_x
    force1_y = 2 * bending_force_constant * (actual_bond_angle - natural_bond_angle) / denominator * numerator1_y
    force1_z = 2 * bending_force_constant * (actual_bond_angle - natural_bond_angle) / denominator * numerator1_z

    force2_x = 2 * bending_force_constant * (actual_bond_angle - natural_bond_angle) / denominator * numerator2_x
    force2_y = 2 * bending_force_constant * (actual_bond_angle - natural_bond_angle) / denominator * numerator2_y
    force2_z = 2 * bending_force_constant * (actual_bond_angle - natural_bond_angle) / denominator * numerator2_z

    force3_x = 2 * bending_force_constant * (actual_bond_angle - natural_bond_angle) / denominator * numerator3_x
    force3_y = 2 * bending_force_constant * (actual_bond_angle - natural_bond_angle) / denominator * numerator3_y
    force3_z = 2 * bending_force_constant * (actual_bond_angle - natural_bond_angle) / denominator * numerator3_z


    force1 = Vector3D(force1_x, force1_y, force1_z)
    force2 = Vector3D(force2_x, force2_y, force2_z)
    force3 = Vector3D(force3_x, force3_y, force3_z)

    atom1.force += force1
    atom2.force += force2
    atom3.force += force3

def coloumb(atom1: Atom, atom2: Atom, k=10**10):
    distance = atom1.position - atom2.position
    force = (distance / distance.norm()**3) * k * (atom1.charge * atom2.charge)

    atom1.force += force
    atom2.force -= force

def dihedral_angle_torsion(atom1: Atom, atom2: Atom, atom3: Atom, atom4: Atom, barrier: float, periodicity: float):
    torsion_angle = 0

    potential =  (1 + cos(periodicity * torsion_angle)) / (2* barrier)
    return potential
