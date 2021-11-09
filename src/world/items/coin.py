from src.world.items.item import Item
from src.world.base_sprite import DrawableSprite


class Coin(DrawableSprite, Item):
    BRONZE_VALUE = 1
    SILVER_VALUE = 2
    GOLD_VALUE = 3
    SFX = 'pickup_coin.wav'

    def __init__(self, x, y, value, image_name, groups):
        DrawableSprite.__init__(self, groups, default_image_name=image_name, shared=True)
        Item.__init__(self, groups)
        self._value = value
        self.rect.topleft = x, y

        # Shrink the hit box.
        self.hit_rect = self.rect.copy()
        self.hit_rect.width /= 2
        self.hit_rect.height /= 2
        self.hit_rect.center = self.rect.center

    def affect(self, player):
        DrawableSprite.get_sound_player().play_sfx(Coin.SFX)
        player.coins += self._value
        super().kill()

    @classmethod
    def create(cls, x, y, coin_type, groups):
        if coin_type == 'bronze':
            return Coin(x, y, Coin.BRONZE_VALUE, 'coinBronze.png', groups)
        elif coin_type == 'silver':
            return Coin(x, y, Coin.SILVER_VALUE, 'coinSilver.png', groups)
        elif coin_type == 'gold':
            return Coin(x, y, Coin.GOLD_VALUE, 'coinGold.png', groups)
        raise ValueError(f"Invalid coin type: '{coin_type}'")


DrawableSprite.get_sound_player().get_sfx(Coin.SFX).set_volume(0.1)
