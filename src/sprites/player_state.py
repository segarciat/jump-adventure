import abc

import src.input.input_manager as input_manager
import src.world.physics as physics
from src.utils.timer import Timer


class PlayerState:
    def __init__(self, player):
        self._player = player

    @abc.abstractmethod
    def enter(self) -> None:
        """Alter height based on the image in current frame."""
        self._player.hit_rect.height = self._player.rect.height

    @abc.abstractmethod
    def handle_keys(self) -> None:
        """Handles state transition depending on the key that was pressed."""
        pass

    @abc.abstractmethod
    def update(self, dt: float) -> None:
        """Effects the behavior of the sprite based on the current state."""
        pass

    def exit(self) -> None:
        """Optional hook to let the state do any necessary clean-up."""
        pass

    def _fall(self):
        """Causes a sprite to 'fall' by switching to jump state, but retaining original y velocity."""
        vy_0 = self._player.vel.y
        self._player.state = self._player.jump_state
        self._player.vel.y = vy_0


class PlayerStandState(PlayerState):
    def __init__(self, player):
        PlayerState.__init__(self, player)

    def enter(self) -> None:
        self._player.vel.x = 0
        self._player.vel.y = 0
        self._player.acc.x = 0
        if self._player.facing_left:
            self._player.change_anim(self._player.STAND_L)
        else:
            self._player.change_anim(self._player.STAND_R)
        super().enter()

    def handle_keys(self) -> None:
        if input_manager.process_active_binding("right"):
            self._player.facing_left = False
            self._player.state = self._player.walk_state
        elif input_manager.process_active_binding("left"):
            self._player.facing_left = True
            self._player.state = self._player.walk_state
        elif input_manager.process_active_binding("jump"):
            self._player.state = self._player.jump_state
        elif input_manager.process_active_binding("duck"):
            self._player.state = self._player.duck_state

    def update(self, dt: float) -> None:
        """Transitions to jumping if not on the ground."""
        if not physics.on_ground(self._player):
            self._fall()


class PlayerDuckState(PlayerState):
    def __init__(self, player):
        PlayerState.__init__(self, player)

    def enter(self) -> None:
        """Sets ducking animation and resizes the collision rectangle."""
        if self._player.facing_left:
            self._player.change_anim(self._player.DUCK_L)
        else:
            self._player.change_anim(self._player.DUCK_R)
        super().enter()
        self._player.hit_rect.height = int(self._player.rect.height * 0.9)

    def handle_keys(self) -> None:
        if not input_manager.process_active_binding("duck"):
            self._player.state = self._player.stand_state

    def update(self, dt: float) -> None:
        """Do nothing while ducking."""
        pass


class PlayerWalkState(PlayerState):
    SPEED = 250

    def __init__(self, player):
        PlayerState.__init__(self, player)

    def enter(self) -> None:
        """Switches to walking animation and sets walking velocity."""
        if self._player.facing_left:
            self._player.change_anim(self._player.WALK_L)
            self._player.vel.x = -PlayerWalkState.SPEED
        else:
            self._player.change_anim(self._player.WALK_R)
            self._player.vel.x = PlayerWalkState.SPEED
        super().enter()

    def handle_keys(self) -> None:
        if not self._player.facing_left and not input_manager.process_active_binding("right"):
            self._player.state = self._player.stand_state
        elif self._player.facing_left and not input_manager.process_active_binding("left"):
            self._player.state = self._player.stand_state
        elif input_manager.process_active_binding("jump"):
            self._player.state = self._player.jump_state

    def update(self, dt: float) -> None:
        """Update image to face correct direction (left or right), and checks if sprite is falling"""
        if not physics.on_ground(self._player):
            self._fall()
        else:
            self._player.update_anim(dt)


class PlayerJumpState(PlayerState):
    JUMP = 1200
    TURN_SPEED = PlayerWalkState.SPEED * 0.5

    def __init__(self, player):
        PlayerState.__init__(self, player)

    def enter(self) -> None:
        if self._player.facing_left:
            self._player.change_anim(self._player.JUMP_L)
        else:
            self._player.change_anim(self._player.JUMP_R)
        self._player.vel.y = -PlayerJumpState.JUMP
        super().enter()

    def handle_keys(self):
        """Allows the player to turn in the air, slowing them down a bit if they turn"""
        if self._player.facing_left and input_manager.process_active_binding("right"):
            self._player.facing_left = False
            self._player.change_anim(self._player.JUMP_R)
            # self._player.vel.x += abs(self._player.vel.x) / 2
        elif not self._player.facing_left and input_manager.process_active_binding("left"):
            self._player.facing_left = True
            self._player.change_anim(self._player.JUMP_L)
            # self._player.vel.x -= abs(self._player.vel.x) / 2

    def update(self, dt: float):
        """If player reaches floor, go to standing state"""
        if physics.on_ground(self._player):
            self._player.state = self._player.stand_state


class PlayerHurtState(PlayerState):
    HURT_DURATION = 250

    def __init__(self, player):
        PlayerState.__init__(self, player)
        self._hurt_timer = Timer()

    def enter(self) -> None:
        if self._player.facing_left:
            self._player.change_anim(self._player.HURT_L)
        else:
            self._player.change_anim(self._player.HURT_R)
        self._hurt_timer.restart()

    def handle_keys(self) -> None:
        pass

    def update(self, dt: float) -> None:
        if self._hurt_timer.elapsed() > PlayerHurtState.HURT_DURATION:
            self._player.state = self._player.stand_state
