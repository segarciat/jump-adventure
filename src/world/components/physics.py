import pygame as pg

import src.config as cfg


class PhysicsComponent:
    def __init__(self, sprite, x, y, forces, collision_handlers):
        center_x, bottom_y = x + sprite.rect.w / 2, y + sprite.rect.h
        self.pos = pg.Vector2(center_x, bottom_y)
        self.vel = pg.Vector2(0, 0)
        self.acc = pg.Vector2(0, 0)
        sprite.hit_rect.midbottom = center_x, bottom_y

        self.forces = forces
        self._sprite = sprite
        self._collision_handlers = collision_handlers

    def update(self, *args, **kwargs) -> None:
        for force in self.forces:
            force(self.pos, self.vel, self.acc)
        self.vel += self.acc * cfg.MS_PER_UPDATE
        displacement = (self.vel * cfg.MS_PER_UPDATE) + (0.5 * self.acc * cfg.MS_PER_UPDATE ** 2)

        # Move and collide in y direction.
        self.pos.y += int(displacement.y)
        self._sprite.hit_rect.bottom = self.pos.y
        for collision_handler in self._collision_handlers:
            collision_handler['callback'](self._sprite, collision_handler['colliders'], displacement)

            # Move and collide in x direction.
        self.pos.x += int(displacement.x)
        self._sprite.hit_rect.centerx = self.pos.x
        for collision_handler in self._collision_handlers:
            collision_handler['callback'](self._sprite, collision_handler['colliders'], displacement)
