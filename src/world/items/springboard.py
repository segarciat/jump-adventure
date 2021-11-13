import src.config as cfg

from src.world.items.item import Item
from src.world.base_sprite import DrawableSprite, IUpdatable
from src.utils.timer import Timer


class SpringBoard(DrawableSprite, Item, IUpdatable):
    JUMP_VEL = 2000
    SPRING_COMPRESS = 14
    DELAY = 150
    PADDING = 20
    UP_IMAGE = 'springboardUp.png'
    DOWN_IMAGE = 'springboardDown.png'

    def __init__(self, x, y, groups):
        DrawableSprite.__init__(self, groups, default_image_name=SpringBoard.UP_IMAGE, shared=True)
        IUpdatable.__init__(self, groups)
        Item.__init__(self, groups)
        # Removed while sprung up; re-add when sprung down, since update only matters while sprung down.
        self._update_group = groups[cfg.UPDATE_GROUP]
        self._update_group.remove(self)
        self._spring_up_surface = self.image
        self._spring_down_surface = DrawableSprite.get_image(SpringBoard.DOWN_IMAGE, shared=True)
        self.rect.topleft = x, y
        self.hit_rect = self.rect.copy()
        self.hit_rect.topleft = x, y + SpringBoard.PADDING
        self.hit_rect.height -= SpringBoard.PADDING
        self._player = None
        self._activation_timer = Timer()
        self._activation_timer.pause()

    def update(self, *args, **kwargs):
        """Springs the board back up after a short delay."""
        if self._activation_timer.elapsed() >= SpringBoard.DELAY:
            self.image = self._spring_up_surface
            self._activation_timer.restart()
            self._activation_timer.pause()
            self._update_group.remove(self)

    def affect(self, player):
        """Sets the player's y velocity to effect a powerful jump by the player."""
        if player.sprite.physics.vel.y > 0:
            self.image = self._spring_down_surface
            player.sprite.physics.vel.y = -SpringBoard.JUMP_VEL
            # todo: testing this effect.
            # player.sprite.physics.vel.x = 0
            # print(f'before: {player.sprite.physics.acc.x}')
            # player.sprite.physics.acc.x = 0
            # print(f'after:{player.sprite.physics.acc.x}')
            self._activation_timer.unpause()
            self._update_group.add(self)
        # todo: Check whether collision happened from left or right or something else?
