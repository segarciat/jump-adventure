import pygame as pg
import abc

import src.config as cfg
import src.services.image_loader as image_loader
import src.services.sound as sound_player


class DrawableSprite(pg.sprite.Sprite, metaclass=abc.ABCMeta):
    """An abstract base class that derives from the pygame Sprite class."""
    def __init__(self, groups: dict[str, pg.sprite.Group], default_image_name: str, shared: bool = False):
        pg.sprite.Sprite.__init__(self, groups[cfg.DRAW_GROUP])
        self._image = image_loader.get_image(default_image_name, shared)
        self.rect = self._image.get_rect()
        self.hit_rect = self.rect.copy()

    @property
    def image(self) -> pg.Surface:
        return self._image

    @image.setter
    def image(self, new_image: pg.Surface) -> None:
        """Updates the Sprite's image along with its rectangle's dimensions, but preserves bottom anchor."""
        self._image = new_image
        self.rect.width = new_image.get_width()
        self.rect.height = new_image.get_height()
        self.rect.midbottom = self.hit_rect.midbottom

    def draw(self, screen: pg.Surface, camera):
        """Draws sprite's image at an offset of the world's camera rectangle."""
        screen.blit(self._image, camera.apply(self.rect))

    @staticmethod
    def get_image(name: str, shared: bool = False) -> pg.Surface:
        return image_loader.get_image(name, shared)

    @staticmethod
    def get_sound_player():
        return sound_player


class IUpdatable(metaclass=abc.ABCMeta):
    """Interface for sprites that are to be updated every frame of the game loop."""
    def __init__(self, groups):
        groups[cfg.UPDATE_GROUP].add(self)

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        pass
