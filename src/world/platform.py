import pygame as pg


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, *groups):
        # todo: decide if keep platforms group, and whether to subclass BaseSprite
        pg.sprite.Sprite.__init__(self, *groups)
        self.hit_rect = pg.Rect(x, y, w, h)
