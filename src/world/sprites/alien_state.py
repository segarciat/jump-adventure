import abc

import src.world.physics as physics
from src.state import IState
from src.utils.timer import Timer


class AlienState(IState, metaclass=abc.ABCMeta):
    def __init__(self, alien):
        self._alien = alien

    @abc.abstractmethod
    def enter(self) -> None:
        self._alien.hit_rect.height = self._alien.rect.height

    @abc.abstractmethod
    def update(self, *args, **kwargs) -> None:
        """Effects the behavior of the sprite based on the current state."""
        pass

    def _fall(self):
        """Causes a sprite to 'fall' by switching to jump state, but retaining original y velocity."""
        vy_0 = self._alien.physics.vel.y
        self._alien.state = self._alien.jump_state
        self._alien.physics.vel.y = vy_0


class AlienStandState(AlienState):
    def __init__(self, alien):
        AlienState.__init__(self, alien)

    def enter(self) -> None:
        self._alien.physics.vel.x = 0
        self._alien.physics.vel.y = 0
        self._alien.physics.acc.x = 0
        if self._alien.facing_left:
            self._alien.change_anim(self._alien.STAND_L)
        else:
            self._alien.change_anim(self._alien.STAND_R)
        super().enter()

    def update(self, *args, **kwargs) -> None:
        """Transitions to jumping if not on the ground."""
        if not physics.on_ground(self._alien, world=kwargs['world']):
            self._fall()


class AlienDuckState(AlienState):
    def __init__(self, alien):
        AlienState.__init__(self, alien)

    def enter(self) -> None:
        """Sets ducking animation and resizes the collision rectangle."""
        if self._alien.facing_left:
            self._alien.change_anim(self._alien.DUCK_L)
        else:
            self._alien.change_anim(self._alien.DUCK_R)
        super().enter()
        self._alien.hit_rect.height = int(self._alien.rect.height * 0.9)

    def update(self, *args, **kwargs) -> None:
        """Do nothing while ducking."""
        pass


class AlienWalkState(AlienState):
    SPEED = 250

    def __init__(self, alien):
        AlienState.__init__(self, alien)

    def enter(self) -> None:
        """Switches to walking animation and sets walking velocity."""
        if self._alien.facing_left:
            self._alien.change_anim(self._alien.WALK_L)
            self._alien.physics.vel.x = -AlienWalkState.SPEED
        else:
            self._alien.change_anim(self._alien.WALK_R)
            self._alien.physics.vel.x = AlienWalkState.SPEED
        super().enter()

    def update(self, *args, **kwargs) -> None:
        """Update image to face correct direction (left or right), and checks if sprite is falling"""
        if not physics.on_ground(self._alien, world=kwargs['world']):
            self._fall()
        else:
            self._alien.update_anim()


class AlienJumpState(AlienState):
    JUMP = 1200
    TURN_SPEED = AlienWalkState.SPEED * 0.5

    def __init__(self, alien):
        AlienState.__init__(self, alien)

    def enter(self) -> None:
        if self._alien.facing_left:
            self._alien.change_anim(self._alien.JUMP_L)
        else:
            self._alien.change_anim(self._alien.JUMP_R)
        self._alien.physics.vel.y = -AlienJumpState.JUMP
        super().enter()

    def update(self, *args, **kwargs):
        """If alien reaches floor, go to standing state"""
        if physics.on_ground(self._alien, world=kwargs['world']):
            self._alien.state = self._alien.stand_state


class AlienHurtState(AlienState):
    HURT_DURATION = 250

    def __init__(self, alien):
        AlienState.__init__(self, alien)
        self._hurt_timer = Timer()

    def enter(self) -> None:
        if self._alien.facing_left:
            self._alien.change_anim(self._alien.HURT_L)
        else:
            self._alien.change_anim(self._alien.HURT_R)
        self._hurt_timer.restart()

    def update(self, *args, **kwargs) -> None:
        if self._hurt_timer.elapsed() > AlienHurtState.HURT_DURATION:
            self._alien.state = self._alien.stand_state
