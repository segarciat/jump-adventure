import pygame as pg
import random

import src.world.physics as physics
from src.world.animated_sprite import AnimatedSprite
from src.world.base_sprite import IUpdatable
from src.world.components.physics import PhysicsComponent


class Slime(AnimatedSprite, IUpdatable):
    # Slime frames.
    WALK_L = 0
    DEAD_L = 2
    WALK_R = 1
    DEAD_R = 3

    TURN_CHANCE = 0.01
    BASE_VELOCITY = 100

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

        # Animation frame rate.
        self._anim_fps = 4.0

        self.facing_left = True
        self.physics.vel.x = -Slime.BASE_VELOCITY
        self._turn()

    @property
    def direction(self) -> int:
        """ -1 for left, 1 for right."""
        return -1 if self.facing_left else 1

    def update(self, *args, **kwargs) -> None:
        # In case slime hit a wall, reset velocity.
        self.physics.vel.x = Slime.BASE_VELOCITY * self.direction
        self._turn()
        self.physics.update()
        self.update_anim()

    def _turn(self) -> None:
        """Have the slime turn around with a 1% chance."""
        if random.random() < Slime.TURN_CHANCE:
            self.physics.vel.x *= -1
            self.facing_left = not self.facing_left
            if self.facing_left:
                self.change_anim(Slime.WALK_L)
            else:
                self.change_anim(Slime.WALK_R)
