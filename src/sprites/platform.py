import pygame as pg


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, all_groups):
        pg.sprite.Sprite.__init__(self, all_groups['all'])
        self.image = pg.Surface((w, h))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.rect.x = x
        self.rect.y = y
