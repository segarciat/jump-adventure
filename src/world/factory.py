import src.config as cfg

from src.world.sprites.alien import Alien
from src.world.sprites.platform import Platform

# Item sprites.
from src.world.sprites.items.coin import Coin
from src.world.sprites.items.springboard import SpringBoard
from src.world.sprites.items.spikes import Spikes
from src.world.sprites.items.weight import ChainedWeight


class Factory:
    @classmethod
    def create(cls, p, player, groups):
        if p.name == "alien":
            return Factory.create_alien(p, groups)
        elif p.name == "platform":
            return Factory.create_platform(p, groups)
        elif p.name == "step":
            return Factory.create_step(p, groups)
        elif p.name == "coin":
            return Factory.create_coin(p, groups)
        elif p.name == "spikes":
            return Factory.create_spikes(p, groups)
        elif p.name == "springboard":
            return Factory.create_springboard(p, groups)
        elif p.name == "weight":
            return Factory.create_weight(p, player, groups)

    @classmethod
    def create_alien(cls, p, groups):
        return Alien(p.x, p.y, Alien.GREEN, groups)

    @classmethod
    def create_platform(cls, p, groups):
        return Platform(p.x, p.y, p.width, p.height, groups[cfg.PLATFORM_GROUP], groups[cfg.OBSTACLE_GROUP])

    @classmethod
    def create_step(cls, p, groups):
        return Platform(p.x, p.y, p.width, p.height, groups[cfg.STEPS_GROUP])

    @classmethod
    def create_coin(cls, p, groups):
        return Coin.create(p.x, p.y, p.coin_type, groups)

    @classmethod
    def create_spikes(cls, p, groups):
        return Spikes(p.x, p.y, groups)

    @classmethod
    def create_springboard(cls, p, groups):
        return SpringBoard(p.x, p.y, groups)

    @classmethod
    def create_weight(cls, p, player, groups):
        return ChainedWeight(p.x, p.y, player, groups)
