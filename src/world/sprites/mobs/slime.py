import pygame as pg
import random

import src.world.physics as physics
from src.world.sprites.animated_sprite import AnimatedSprite
from src.world.sprites.base_sprite import IUpdatable
from src.world.sprites.components.physics import PhysicsComponent


class Slime(AnimatedSprite, IUpdatable):
    WALK_L = 0
    DEAD_L = 2
    WALK_R = 1
    DEAD_R = 3

    def __init__(self, x, y, groups):
        frames = [
            {'animation_number': Slime.WALK_L, 'image_names': ['slimeWalk1.png', 'slimeWalk2.png']},
            {'animation_number': Slime.DEAD_L, 'image_names': ['slimeDead.png']},
            {'animation_number': Slime.WALK_R, 'image_names': ['slimeWalk1.png', 'slimeWalk2.png']},
            {'animation_number': Slime.DEAD_R, 'image_names': ['slimeDead.png']},
        ]
        AnimatedSprite.__init__(self, frames, groups)
        IUpdatable.__init__(self, groups)

        for animation in (Slime.WALK_R, Slime.DEAD_R):
            for frame, image in enumerate(self._images[animation]):
                self._images[animation][frame] = pg.transform.flip(image, True, False)
        print(self._images)
        self.physics = PhysicsComponent(
            sprite=self,
            x=x,
            y=y,
            forces=[physics.apply_gravity],
            collision_handlers=[
                {'callback': physics.halt_collide_y, 'colliders': groups['obstacles']},
                {'callback': physics.halt_collide_x, 'colliders': groups['obstacles']},
                {'callback': physics.step_collision, 'colliders': groups['steps']}
            ],
        )
        self.hit_rect.midbottom = x, y

        self.facing_left = True
        self.physics.vel.x = -100
        self._anim_fps = 8.0  # Animation frame rate.
        self.change_anim(Slime.WALK_L)

    def update_anim(self):
        super().update_anim()
        self.rect.midbottom = self.physics.pos

    def update(self, *args, **kwargs):
        # Have the slime turn around with a 1% chance.
        if random.random() < 0.01:
            self.physics.vel.x *= -1
            self.facing_left = not self.facing_left
            if self.facing_left:
                self.change_anim(Slime.WALK_L)
            else:
                self.change_anim(Slime.WALK_R)
        self.physics.update()
        self.update_anim()
