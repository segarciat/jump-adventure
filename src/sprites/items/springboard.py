from src.sprites.items.base_item import BaseItem
from src.sprites.animated_sprite import AnimatedSprite
from src.utils.timer import Timer


class SpringBoard(AnimatedSprite, BaseItem):
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
        self._activation_timer = Timer()
        self._activation_timer.pause()

    def update(self, dt: float):
        """Springs the board back up after a short delay."""
        if self._activation_timer.elapsed() >= SpringBoard.DELAY:
            self.change_anim(SpringBoard.SPRING_UP)
            self.hit_rect.y -= SpringBoard.SPRING_COMPRESS
            self._activation_timer.restart()
            self._activation_timer.pause()

    def collide(self, player):
        """Sets the player's y velocity to effect a powerful jump by the player."""
        if player.vel.y > 0:
            player.vel.y = -SpringBoard.JUMP_VEL
            self.change_anim(SpringBoard.SPRING_DOWN)
            self.hit_rect.y += SpringBoard.SPRING_COMPRESS
            self._activation_timer.unpause()
