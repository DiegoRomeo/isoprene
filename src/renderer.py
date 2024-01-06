import pygame

from vmath import Vector3D, isometric

class RendererISO(object):

    @staticmethod
    def render(display: pygame.Surface, surface: pygame.Surface, position: Vector3D, scale_factor=1):
        width, height = display.get_size()
        surface_width, surface_height = surface.get_size()

        x, y = map(int, isometric(position))

        x, y = x * scale_factor, y * scale_factor
        display.blit(surface, (x + width // 2 - surface_width // 2, height - (y + height // 2) + surface_height // 2))
