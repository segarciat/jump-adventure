import pygame as pg

import src.world.physics as physics
from src.state import StatefulMixin
from src.world.sprites.base_sprite import IUpdatable
from src.world.sprites.animated_sprite import AnimatedSprite
from src.world.sprites.components.physics import PhysicsComponent
from src.world.sprites.alien_state import AlienState, AlienDuckState, AlienJumpState, AlienStandState, AlienWalkState, \
    AlienHurtState


class Alien(AnimatedSprite, IUpdatable, StatefulMixin):
    # Index corresponding to each different color alien.
    GREEN = 1
    BLUE = 2
    PINK = 3

    # Animation numbers.
    STAND_R = 0
    DUCK_R = 1
    FRONT_R = 2
    HURT_R = 3
    JUMP_R = 4
    WALK_R = 5

    STAND_L = 6
    DUCK_L = 7
    FRONT_L = 8
    HURT_L = 9
    JUMP_L = 10
    WALK_L = 11

    MAX_HEARTS = 3

    def __init__(self, x: float, y: float, alien_color: int, groups):
        frames = [
            # Right frames.
            {'animation_number': Alien.STAND_R, 'image_names': [f'p{alien_color}_stand.png']},
            {'animation_number': Alien.DUCK_R, 'image_names': [f'p{alien_color}_duck.png']},
            {'animation_number': Alien.FRONT_R, 'image_names': [f'p{alien_color}_front.png']},
            {'animation_number': Alien.HURT_R, 'image_names': [f'p{alien_color}_hurt.png']},
            {'animation_number': Alien.JUMP_R, 'image_names': [f'p{alien_color}_jump.png']},
            {
                'animation_number': Alien.WALK_R,
                'image_names': [f'p{alien_color}_walk{0 if i < 10 else ""}{i}.png' for i in range(1, 12)]
            },
            # Left frames.
            {'animation_number': Alien.STAND_L, 'image_names': [f'p{alien_color}_stand.png']},
            {'animation_number': Alien.DUCK_L, 'image_names': [f'p{alien_color}_duck.png']},
            {'animation_number': Alien.FRONT_L, 'image_names': [f'p{alien_color}_front.png']},
            {'animation_number': Alien.HURT_L, 'image_names': [f'p{alien_color}_hurt.png']},
            {'animation_number': Alien.JUMP_L, 'image_names': [f'p{alien_color}_jump.png']},
            {
                'animation_number': Alien.WALK_L,
                'image_names': [f'p{alien_color}_walk{0 if i < 10 else ""}{i}.png' for i in range(1, 12)]
            },
        ]
        AnimatedSprite.__init__(self, frames, groups)
        IUpdatable.__init__(self, groups)
        StatefulMixin.__init__(self)

        # Flip images corresponding to left frames.
        for animation in (Alien.STAND_L, Alien.DUCK_L, Alien.FRONT_L, Alien.HURT_L, Alien.JUMP_L, Alien.WALK_L):
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

        # Decides the correct image used for the Alien; can be one of Alien.P1, Alien.P2, or Alien.P3.
        self.alien_color = alien_color

        self.max_hearts = Alien.MAX_HEARTS
        self.hearts = self.max_hearts

        # Adjusted hit box for the Alien.
        self.hit_rect = self.rect.copy()
        self.hit_rect.width = int(self.rect.width * 0.7)
        self.hit_rect.midbottom = self.rect.midbottom

        # Alien faces right by default.
        self.facing_left = False

        # Allowable states for the Alien.
        self._stand_state = AlienStandState(self)
        self._duck_state = AlienDuckState(self)
        self._walk_state = AlienWalkState(self)
        self._jump_state = AlienJumpState(self)
        self._hurt_state = AlienHurtState(self)
        self._state = self._stand_state
        self._state.enter()

    @property
    def stand_state(self) -> AlienState:
        return self._stand_state

    @property
    def duck_state(self) -> AlienState:
        return self._duck_state

    @property
    def walk_state(self) -> AlienState:
        return self._walk_state

    @property
    def jump_state(self) -> AlienState:
        return self._jump_state

    @property
    def hurt_state(self) -> AlienState:
        return self._hurt_state

    def change_anim(self, animation_number: int) -> None:
        """Preserves the previous frame's midbottom position when switching animations."""
        old_pos = self.rect.midbottom
        super().change_anim(animation_number)
        self.rect.height = self.image.get_height()
        self.rect.width = self.image.get_width()
        self.rect.midbottom = self.hit_rect.midbottom = old_pos

    def hurt(self, half_heart_damage: int):
        if half_heart_damage <= 0:
            raise ValueError(f'Invalid number of half hearts damage value: {half_heart_damage}')
        # Number of half hearts worth of damage.
        self.hearts -= half_heart_damage * 0.5
        if self.hearts <= 0:
            self.hearts = self.max_hearts
        self.state = self._hurt_state

    def update(self, *args, **kwargs) -> None:
        self.physics.update(*args, **kwargs)
        self._state.update(*args, **kwargs)
