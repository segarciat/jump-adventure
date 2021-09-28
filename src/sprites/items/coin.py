from src.sprites.items.base_item import BaseItem
from src.sprites.base_sprite import BaseSprite


class Coin(BaseSprite, BaseItem):
    BRONZE_VALUE = 1
    SILVER_VALUE = 2
    GOLD_VALUE = 3
    SFX = 'pickup_coin.wav'

    def __init__(self, x, y, value, image, all_groups):
        BaseSprite.__init__(self, image, all_groups, all_groups['all'])
        self._value = value
        self.rect.topleft = x, y
        self.hit_rect.width /= 2
        self.hit_rect.height /= 2
        self.hit_rect.center = self.rect.center

    def collide(self, player):
        BaseSprite.get_sound_player().play_sfx(Coin.SFX)
        player.coins += self._value
        self.kill()

    @classmethod
    def bronze(cls, x, y, all_groups):
        return Coin(x, y, Coin.BRONZE_VALUE, 'coinBronze.png', all_groups)

    @classmethod
    def silver(cls, x, y, all_groups):
        return Coin(x, y, Coin.SILVER_VALUE, 'coinSilver.png', all_groups)

    @classmethod
    def gold(cls, x, y, all_groups):
        return Coin(x, y, Coin.GOLD_VALUE, 'coinGold.png', all_groups)


BaseSprite.get_sound_player().get_sfx(Coin.SFX).set_volume(0.1)
