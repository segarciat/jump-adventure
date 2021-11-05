from src.world.sprites.items.item import Item
from src.world.sprites.base_sprite import DrawableSprite


class Spikes(DrawableSprite, Item):
    DAMAGE = 1

    def __init__(self, x, y, groups):
        DrawableSprite.__init__(self, groups, default_image_name='spikes.png', shared=True)
        Item.__init__(self, groups)
        self.rect.topleft = x, y

        # Shrink the hit box.
        self.hit_rect = self.rect.copy()
        self.hit_rect.height /= 2
        self.hit_rect.topleft = x, y + self.hit_rect.height

    def affect(self, player):
        if player.sprite.state != player.sprite.hurt_state:
            player.sprite.hurt(Spikes.DAMAGE)
            # Knock-back player.
            if player.sprite.physics.pos.x > self.rect.centerx:
                player.sprite.physics.vel.xy = 300, -300
            else:
                player.sprite.physics.vel.xy = -300, -300
