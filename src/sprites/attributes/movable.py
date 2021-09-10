import pygame as pg
import typing

from src.sprites.base_sprite import BaseSprite


class MoveMixin:
    """Mix-in class that an object whose class derives from BaseSprite would subclass to obtain move behavior."""
    def __init__(self: typing.Union[BaseSprite, 'MoveMixin'], x: float, y: float):
        """Assigns a position, velocity, and acceleration vector to sprite."""
        self.pos = pg.math.Vector2(x, y)
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)
        self.rect.midbottom = self.pos
        self.hit_rect.midbottom = self.pos

    def move(self: typing.Union[BaseSprite, 'MoveMixin'], dt: float, collision_handler=None):
        """Updates the acceleration, velocity, and position of this object, and handles collisions."""
        # Effect kinematic equations.
        self.vel += self.acc * dt
        displacement = (self.vel * dt) + (0.5 * self.acc * dt**2)
        if collision_handler:
            collision_handler(self, displacement)
