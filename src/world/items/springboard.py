from src.world.items.item import Item
from src.world.base_sprite import DrawableSprite, IUpdatable
from src.utils.timer import Timer


class SpringBoard(DrawableSprite, Item, IUpdatable):
    JUMP_VEL = 2000
    SPRING_COMPRESS = 14
    DELAY = 150
    UP_IMAGE = 'springboardUp.png'
    DOWN_IMAGE = 'springboardDown.png'

    def __init__(self, x, y, groups):
        DrawableSprite.__init__(self, groups, default_image_name=SpringBoard.UP_IMAGE, shared=True)
        IUpdatable.__init__(self, groups)
        Item.__init__(self, groups)
        # Removed while sprung up; re-add when sprung down, since update only matters while sprung down.
        self._update_group = groups[IUpdatable.GROUP_NAME]
        self._update_group.remove(self)
        self._spring_up_surface = self.image
        self._spring_down_surface = DrawableSprite.get_image(SpringBoard.DOWN_IMAGE, shared=True)
        self.rect.topleft = x, y
        self.hit_rect = self.rect.copy()
        self.hit_rect.topleft = x, y + 20
        self._player = None
        self._activation_timer = Timer()
        self._activation_timer.pause()

    def update(self, *args, **kwargs):
        """Springs the board back up after a short delay."""
        if self._activation_timer.elapsed() >= SpringBoard.DELAY:
            self.image = self._spring_up_surface
            self.hit_rect.y -= SpringBoard.SPRING_COMPRESS
            self._activation_timer.restart()
            self._activation_timer.pause()
            self._update_group.remove(self)

    def affect(self, player):
        """Sets the player's y velocity to effect a powerful jump by the player."""
        if player.sprite.physics.vel.y > 0:
            player.sprite.physics.vel.y = -SpringBoard.JUMP_VEL
            self.image = self._spring_down_surface
            self.hit_rect.y += SpringBoard.SPRING_COMPRESS
            self._activation_timer.unpause()
            self._update_group.add(self)
        # todo: Check whether collision happened from left or right or something else?
