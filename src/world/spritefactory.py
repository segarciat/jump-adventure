import src.config as cfg

from src.world.alien import Alien
from src.world.platform import Platform

from src.world.mobs.slime import Slime
from src.world.mobs.fish import Fish

# Item sprites.
from src.world.items.coin import Coin
from src.world.items.springboard import SpringBoard
from src.world.items.spikes import Spikes
from src.world.items.weight import ChainedWeight


class SpriteFactory:
    @classmethod
    def create(cls, p, player, groups):
        if p.name == "alien":
            return SpriteFactory.create_alien(p, groups)
        elif p.name == "platform":
            return SpriteFactory.create_platform(p, groups)
        elif p.name == "step":
            return SpriteFactory.create_step(p, groups)
        elif p.name == "coin":
            return SpriteFactory.create_coin(p, groups)
        elif p.name == "spikes":
            return SpriteFactory.create_spikes(p, groups)
        elif p.name == "springboard":
            return SpriteFactory.create_springboard(p, groups)
        elif p.name == "weight":
            return SpriteFactory.create_weight(p, player, groups)
        elif p.name == "fish":
            pass
        elif p.name == "slime":
            return SpriteFactory.create_slime(p, groups)

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

    @classmethod
    def create_slime(cls, p, groups):
        x = p.x + p.width / 2
        y = p.y + p.height
        return Slime(x, y, groups)

    @classmethod
    def create_fish(cls, p, groups):
        x = p.x + p.width / 2
        y = p.y + p.height
        return Fish(x, y, groups)