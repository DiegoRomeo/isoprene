import sys
import pygame
from pygame.locals import *

from pathlib import Path

from vmath import Vector3D
from simulation import Simulation
from entities import Atom, Bond, Angle, Molecule
from renderer import RendererISO

from math import degrees, radians

"""
length: angstroms
time: ps
mass: dalton
"""

SCALE_FACTOR = 1

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption("PolyIsoprene simulation")
screen = pygame.display.set_mode((900,900), SCALED + RESIZABLE)
display = pygame.Surface((900, 900))

blue_ball_path = Path("../assets/images/hydrogen.png").resolve()
blue_ball = pygame.image.load(blue_ball_path)
#blue_ball.set_colorkey((, 0, 0))
blue_ball = pygame.transform.scale(blue_ball, (30, 30))

red_ball_path = Path("../assets/images/oxygen.png").resolve()
red_ball = pygame.image.load(red_ball_path)
#red_ball.set_colorkey((0, 0, 0))
red_ball = pygame.transform.scale(red_ball, (60, 60))


iso_path = Path("../assets/images/iso.png").resolve()
iso = pygame.image.load(iso_path).convert()
iso.set_colorkey((0, 0, 0))
iso = pygame.transform.scale(iso, (200, 200))


sigma = 0.02
epsilon = 1

h_sigma = sigma
h_epsilon = epsilon

hydrogen1 = Atom(mass=1.008, position=Vector3D(3, 0.5, 0), interaction_radius=h_sigma, interaction_strength=h_epsilon, image=blue_ball)
hydrogen2 = Atom(mass=1.008, position=Vector3D(3, -0.5, 0), interaction_radius=h_sigma, interaction_strength=h_epsilon, image=blue_ball)
hydrogen3 = Atom(mass=1.008, position=Vector3D(-2, -1, 1.2), interaction_radius=h_sigma, interaction_strength=h_epsilon, image=blue_ball)
hydrogen4 = Atom(mass=1.008, position=Vector3D(-5, 0.5, 1), interaction_radius=h_sigma, interaction_strength=h_epsilon, image=blue_ball)
hydrogen5 = Atom(mass=1.008, position=Vector3D(-5, 0.7, -1.3), interaction_radius=h_sigma, interaction_strength=h_epsilon, image=blue_ball)
hydrogen6 = Atom(mass=1.008, position=Vector3D(1, 0, 3), interaction_radius=h_sigma, interaction_strength=h_epsilon, image=blue_ball)
hydrogen7 = Atom(mass=1.008, position=Vector3D(-1.8, 1, 3), interaction_radius=h_sigma, interaction_strength=h_epsilon, image=blue_ball)
hydrogen8 = Atom(mass=1.008, position=Vector3D(0, 1.1, 3.2), interaction_radius=h_sigma, interaction_strength=h_epsilon, image=blue_ball)

carbon1 = Atom(mass=12, position=Vector3D(2, 0.3, 0), interaction_radius=sigma, interaction_strength=epsilon, image=red_ball)
carbon2 = Atom(mass=12, position=Vector3D(0.1, 0, 0.4), interaction_radius=sigma, interaction_strength=epsilon, image=red_ball)
carbon3 = Atom(mass=12, position=Vector3D(-2, 0.5, 0), interaction_radius=sigma, interaction_strength=epsilon, image=red_ball)
carbon4 = Atom(mass=12, position=Vector3D(-4, 1, 0.3), interaction_radius=sigma, interaction_strength=epsilon, image=red_ball)
carbon5 = Atom(mass=12, position=Vector3D(0, 0.7, 2), interaction_radius=sigma, interaction_strength=epsilon, image=red_ball)


k = 2
# CH2 bonds
bond1 = Bond(carbon1, hydrogen1, k, 0.5)
bond2 = Bond(carbon1, hydrogen2, k, 0.5)

bond3 = Bond(carbon2, carbon1, k, 50)
bond4 = Bond(carbon2, carbon5, k, 50)
bond5 = Bond(carbon2, carbon3, k, 50)

bond6 = Bond(carbon3, hydrogen3, k, 0.5)
bond7 = Bond(carbon3, carbon4, k, 50)

bond8 = Bond(carbon4, hydrogen4, k, 0.5)
bond9 = Bond(carbon4, hydrogen5, k, 0.5)

bond10 = Bond(carbon5, hydrogen6, k, 0.5)
bond11 = Bond(carbon5, hydrogen7, k, 0.5)
bond12 = Bond(carbon5, hydrogen8, k, 0.5)

k_a = 10

angle1 = Angle(carbon4, carbon3, carbon2, bending_force_constant=k_a, natural_angle=radians(129))
angle2 = Angle(carbon3, carbon2, carbon5, bending_force_constant=k_a, natural_angle=radians(124))
angle3 = Angle(carbon1, carbon2, carbon3, bending_force_constant=k_a, natural_angle=radians(120))
angle4 = Angle(carbon1, carbon2, carbon5, bending_force_constant=k_a, natural_angle=radians(115))
angle5 = Angle(carbon2, carbon1, carbon4, bending_force_constant=k_a, natural_angle=radians(115))
angle6 = Angle(carbon1, carbon4, carbon3, bending_force_constant=k_a, natural_angle=radians(113))

angle7 = Angle(hydrogen6, carbon5, carbon2, bending_force_constant=k_a, natural_angle=radians(110))
angle8 = Angle(hydrogen7, carbon5, carbon2, bending_force_constant=k_a, natural_angle=radians(110))
angle9 = Angle(hydrogen8, carbon5, carbon2, bending_force_constant=k_a, natural_angle=radians(110))


angle10 = Angle(carbon4, carbon3, hydrogen3, bending_force_constant=k_a, natural_angle=radians(114))
angle11 = Angle(carbon2, carbon3, hydrogen3, bending_force_constant=k_a, natural_angle=radians(114))

angle12 = Angle(hydrogen1, carbon1, hydrogen2, bending_force_constant=k_a, natural_angle=radians(110))
angle13 = Angle(hydrogen4, carbon4, hydrogen5, bending_force_constant=k_a, natural_angle=radians(110))


bonds = [bond1, bond2, bond3, bond4, bond5, bond6, bond7, bond8, bond9, bond10, bond11, bond12]
angles = [angle1, angle2, angle3, angle4, angle5, angle6, angle7, angle8, angle9, angle10, angle11, angle12, angle13]

isoprene = Molecule(bonds=bonds, angles=angles)


simulation = Simulation()
simulation.add_atom(hydrogen1)
simulation.add_atom(hydrogen2)
simulation.add_atom(hydrogen3)
simulation.add_atom(hydrogen4)
simulation.add_atom(hydrogen5)
simulation.add_atom(hydrogen6)
simulation.add_atom(hydrogen7)
simulation.add_atom(hydrogen8)

simulation.add_atom(carbon1)
simulation.add_atom(carbon2)
simulation.add_atom(carbon3)
simulation.add_atom(carbon4)
simulation.add_atom(carbon5)


simulation.add_molecule(isoprene)


clock = pygame.time.Clock()

objects = [hydrogen1, hydrogen2, hydrogen3, hydrogen4, hydrogen5, hydrogen6, hydrogen7, hydrogen8, carbon1, carbon2, carbon3, carbon4, carbon5]

while True:
    display.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    dt = clock.tick(60) / 1000
    simulation.update(dt)

    print("110", degrees(isoprene.angles[11].actual_angle))

    display.blit(iso, (display.get_size()[0] // 2 - iso.get_size()[0] // 2, display.get_size()[1] // 2 - iso.get_size()[1] // 2))

    objects.sort(key=lambda atom: atom.position.x + atom.position.y)
    for obj in objects:
        RendererISO.render(display, obj.image, obj.position, scale_factor=SCALE_FACTOR)

    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.update()
