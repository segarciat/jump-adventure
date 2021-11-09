import pygame as pg
import abc

import src.services.image_loader as image_loader
import src.services.sound as sound_player


class DrawableSprite(pg.sprite.Sprite, metaclass=abc.ABCMeta):
    """An abstract base class that derives from the pygame Sprite class."""
    GROUP_NAME = 'drawable'

    def __init__(self, groups: dict[str, pg.sprite.Group], default_image_name: str, shared: bool = False):
        pg.sprite.Sprite.__init__(self, groups[DrawableSprite.GROUP_NAME])
        self.image = image_loader.get_image(default_image_name, shared)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect

    def draw(self, screen: pg.Surface, camera):
        """Draws sprite's image at an offset of the world's camera rectangle."""
        screen.blit(self.image, camera.apply(self.rect))

    @staticmethod
    def get_image(name, shared=False) -> pg.Surface:
        return image_loader.get_image(name, shared)

    @staticmethod
    def get_sound_player():
        return sound_player


class IUpdatable(metaclass=abc.ABCMeta):
    GROUP_NAME = 'updatable'
    """Interface for sprites that are to be updated every frame of the game loop."""
    def __init__(self, groups):
        groups['updatable'].add(self)

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        pass
