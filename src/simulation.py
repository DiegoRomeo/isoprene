from entities import Entity, Atom, Molecule
from interactions import InteractionRegistry, Interaction, angle_bending, coloumb, lennard_jones, bond_stretching

class Simulation:

    def __init__(self) -> None:
        self._entities = {"atoms": [], "molecules": []}
        self.interaction_registry = InteractionRegistry()

    @property
    def entities(self):
        return self._entities

    @entities.setter
    def entities(self, _entities):
        self._entities = _entities

    def add_atom(self, atom: Atom):
        for other in self._entities["atoms"]:
            lennard_jones_interaction = Interaction(lennard_jones, atom, other, atom.interaction_radius, atom.interaction_strength)

            self.interaction_registry.add_interaction(lennard_jones_interaction)

            # This fails if molecule has not been created yet
            same_molecule = False
            for molecule in self._entities["molecules"]:
                if atom in molecule.atoms and other in molecule.atoms:
                    same_molecule = True
                    break

            if not same_molecule:
                coloumb_interaction = Interaction(coloumb, atom, other, 0.5)
                self.interaction_registry.add_interaction(coloumb_interaction)


        self._entities["atoms"].append(atom)
            
    def add_molecule(self, molecule: Molecule):

        # bond stretching forces
        for bond in molecule.bonds:
            bond_stretching_interaction = Interaction(bond_stretching, bond.atom, bond.other, bond.potential_strength, bond.natural_length)
            self.interaction_registry.add_interaction(bond_stretching_interaction)

        # angle bending forces
        for angle in molecule.angles:
            angle_bending_interaction = Interaction(angle_bending, angle.atom1, angle.atom2, angle.atom3, angle.bending_force_constant, angle.natural_angle)
            self.interaction_registry.add_interaction(angle_bending_interaction)

        # remove coloumb force between atoms of the same molecule
        for interaction in self.interaction_registry._interactions:
            if interaction.force != coloumb:
                continue

            if interaction.force_args[0] in molecule.atoms and interaction.force_args[1] in molecule.atoms:

                self.interaction_registry.remove_interaction(interaction)
                del interaction

        self._entities["molecules"].append(molecule)

    def remove_entity(self, entity: Entity):
        if isinstance(entity, Atom):
            self._entities["atoms"].remove(entity)
        elif isinstance(entity, Molecule):
            self.entities["molecules"].remove(entity)
        else:
            raise(ValueError)

    def update(self, dt):
        # update interactions (apply forces to all atoms involved in the interactions)
        self.interaction_registry.update_interactions()

        # update the positions  and velocities of the atoms
        for atom in self._entities["atoms"]:
            atom.update(dt)
