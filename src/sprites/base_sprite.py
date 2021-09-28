import pygame as pg
import abc

import src.config as cfg
import src.services.image_loader as image_loader
import src.services.sound as sound_player


class BaseSprite(pg.sprite.Sprite, metaclass=abc.ABCMeta):
    """An abstract base class that derives from the pygame Sprite class."""
    def __init__(self, image: str, all_groups, *groups: pg.sprite.Group):
        """

        :param image: Filename for this sprite's image.
        :param all_groups: A dictionary of sprite groups.
        :param groups: A sequence of sprite groups that this sprite will be added to.
        """
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = image_loader.get_image(image)
        self.image.set_colorkey(cfg.BLACK)
        # Todo: decide if every sprite should have a reference to all groups.
        self.all_groups = all_groups
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect.copy()  # Untransformed rectangle for collision-handling.

    @staticmethod
    def get_image(name):
        return image_loader.get_image(name)

    @staticmethod
    def get_sound_player():
        return sound_player

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))
