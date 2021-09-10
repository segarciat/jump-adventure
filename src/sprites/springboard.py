from src.utils.timer import Timer
from src.sprites.animated_sprite import AnimatedSprite


class SpringBoard(AnimatedSprite):
    JUMP_VEL = 2000
    SPRING_DOWN = 0
    SPRING_UP = 1
    SPRING_COMPRESS = 14
    DELAY = 150

    def __init__(self, x, y, all_groups):
        frames = [
            {'animation_number': SpringBoard.SPRING_DOWN, 'image_names': ['springboardDown.png']},
            {'animation_number': SpringBoard.SPRING_UP, 'image_names': ['springboardUp.png']},
        ]
        AnimatedSprite.__init__(self, frames, all_groups, all_groups['all'])
        self.change_anim(SpringBoard.SPRING_UP)
        self.rect.topleft = x, y
        self.hit_rect.x = x
        self.hit_rect.y = self.rect.y
        self.hit_rect.topleft = x, y + 20
        self._player = None
        self.activation_timer = Timer()
        self.activation_timer.pause()

    def update(self, dt: float):
        """Springs the board back up after a short delay."""
        if self.activation_timer.elapsed() >= SpringBoard.DELAY:
            self.change_anim(SpringBoard.SPRING_UP)
            self.hit_rect.y -= SpringBoard.SPRING_COMPRESS
            self.activation_timer.restart()
            self.activation_timer.pause()

    def activate(self, player):
        """Sets the player's y velocity to effect a powerful jump by the player."""
        if player.vel.y > 0:
            player.vel.y = -SpringBoard.JUMP_VEL
            self.change_anim(SpringBoard.SPRING_DOWN)
            self.hit_rect.y += SpringBoard.SPRING_COMPRESS
            self.activation_timer.unpause()
