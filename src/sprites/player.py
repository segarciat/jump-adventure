import pygame as pg

import src.world.physics as physics
from src.sprites.animated_sprite import AnimatedSprite
from src.sprites.attributes.movable import MoveMixin
from src.sprites.player_state import PlayerState, PlayerDuckState, PlayerJumpState, PlayerStandState, PlayerWalkState, \
    PlayerHurtState
from src.sprites.player_hud import PlayerHud


class Player(AnimatedSprite, MoveMixin):
    # Index corresponding to each different color alien.
    P1 = 1
    P2 = 2
    P3 = 3

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

    def __init__(self, x: float, y: float, player_number: int, all_groups):
        frames = [
            # Right frames.
            {'animation_number': Player.STAND_R, 'image_names': [f'p{player_number}_stand.png']},
            {'animation_number': Player.DUCK_R, 'image_names': [f'p{player_number}_duck.png']},
            {'animation_number': Player.FRONT_R, 'image_names': [f'p{player_number}_front.png']},
            {'animation_number': Player.HURT_R, 'image_names': [f'p{player_number}_hurt.png']},
            {'animation_number': Player.JUMP_R, 'image_names': [f'p{player_number}_jump.png']},
            {
                'animation_number': Player.WALK_R,
                'image_names': [f'p{player_number}_walk{0 if i < 10 else ""}{i}.png' for i in range(1, 12)]
            },
            # Left frames.
            {'animation_number': Player.STAND_L, 'image_names': [f'p{player_number}_stand.png']},
            {'animation_number': Player.DUCK_L, 'image_names': [f'p{player_number}_duck.png']},
            {'animation_number': Player.FRONT_L, 'image_names': [f'p{player_number}_front.png']},
            {'animation_number': Player.HURT_L, 'image_names': [f'p{player_number}_hurt.png']},
            {'animation_number': Player.JUMP_L, 'image_names': [f'p{player_number}_jump.png']},
            {
                'animation_number': Player.WALK_L,
                'image_names': [f'p{player_number}_walk{0 if i < 10 else ""}{i}.png' for i in range(1, 12)]
            },
        ]
        AnimatedSprite.__init__(self, frames, all_groups, all_groups['all'])
        # Flip images corresponding to left frames.
        for animation in (Player.STAND_L, Player.DUCK_L, Player.FRONT_L, Player.HURT_L, Player.JUMP_L, Player.WALK_L):
            for frame, image in enumerate(self._images[animation]):
                self._images[animation][frame] = pg.transform.flip(image, True, False)
        MoveMixin.__init__(self, x + self.rect.width / 2, y + self.rect.height)

        self.player_number = player_number
        self.hud = PlayerHud(self)
        self.coins = 0
        self.lives = 1
        self.max_hearts = Player.MAX_HEARTS
        self.hearts = 3

        self.hit_rect.width = int(self.rect.width * 0.7)
        self.facing_left = False
        self._stand_state = PlayerStandState(self)
        self._duck_state = PlayerDuckState(self)
        self._walk_state = PlayerWalkState(self)
        self._jump_state = PlayerJumpState(self)
        self._hurt_state = PlayerHurtState(self)
        self._state = self._stand_state
        self._state.enter()

    @property
    def state(self) -> PlayerState:
        """Returns the state current driving this object's behavior."""
        return self._state

    @state.setter
    def state(self, state: PlayerState):
        """Allows the current state to clean-up before transition to a new state."""
        self._state.exit()
        self._state = state
        self._state.enter()

    @property
    def stand_state(self) -> PlayerState:
        return self._stand_state

    @property
    def duck_state(self) -> PlayerState:
        return self._duck_state

    @property
    def walk_state(self) -> PlayerState:
        return self._walk_state

    @property
    def jump_state(self) -> PlayerState:
        return self._jump_state

    @property
    def hurt_state(self) -> PlayerState:
        return self._hurt_state

    def handle_keys(self):
        """Handles keys by delegating to the state driving this object's behavior."""
        self._state.handle_keys()

    def change_anim(self, animation_number: int) -> None:
        """Preserves the previous frame's midbottom position when switching animations."""
        old_pos = self.rect.midbottom
        super().change_anim(animation_number)
        # self.rect = self.image.get_rect()
        self.rect.midbottom = old_pos
        self.hit_rect.midbottom = old_pos

    def hurt(self, half_heart_damage):
        if half_heart_damage <= 0 or type(half_heart_damage) != int:
            raise ValueError(f'Invalid number of half hearts damage value: {half_heart_damage}')
        # Number of half hearts worth of damage.
        self.hearts -= half_heart_damage * 0.5
        if self.hearts <= 0:
            self.lives -= 1
            self.hearts = self.max_hearts
            # Todo: handle case where the player runs out of lives.
        self.state = self._hurt_state

    def update(self, dt: float) -> None:
        physics.apply_gravity(self, dt)
        self.move(dt, physics.handle_ground_collision)
        self._state.update(dt)
