from src.sprites.items.base_item import BaseItem
from src.sprites.base_sprite import BaseSprite


class Spikes(BaseSprite, BaseItem):
    DAMAGE = 1

    def __init__(self, x, y, all_groups):
        BaseSprite.__init__(self, 'spikes.png', all_groups, all_groups['all'])
        self.rect.topleft = x, y
        self.hit_rect.height /= 2
        self.hit_rect.topleft = x, y + self.hit_rect.height

    def collide(self, player):
        if player.state != player.hurt_state:
            player.hurt(Spikes.DAMAGE)
            # Knock-back player.
            if player.pos.x > self.rect.centerx:
                player.vel.xy = 300, -300
            else:
                player.vel.xy = -300, -300
