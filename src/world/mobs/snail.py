import pygame as pg

from src.world.animated_sprite import AnimatedSprite


class Snail(AnimatedSprite):
    SHELL_L = 0
    WALK_L = 1
    SHELL_UPSIDE_DOWN_L = 2

    SHELL_R = 3
    WALK_R = 4
    SHELL_UPSIDE_DOWN_R = 5

    def __init__(self, x, y, groups):
        frames = [
            {'animation_number': Snail.SHELL_L, 'image_names': ['snailShell.png']},
            {'animation_number': Snail.WALK_L, 'image_names': ['snailWalk1.png', 'snailWalk2.png']},
            {'animation_number': Snail.SHELL_UPSIDE_DOWN_L, 'image_names': ['snailShell_upside_down.png']},
            {'animation_number': Snail.SHELL_R, 'image_names': ['snailShell.png']},
            {'animation_number': Snail.WALK_R, 'image_names': ['snailWalk1.png', 'snailWalk2.png']},
            {'animation_number': Snail.SHELL_UPSIDE_DOWN_R, 'image_names': ['snailShell_upside_down.png']},
        ]
        AnimatedSprite.__init__(self, frames, groups)
        for animation in (Snail.SHELL_R, Snail.SHELL_R, Snail.SHELL_UPSIDE_DOWN_R):
            for frame, image in enumerate(self._images[animation]):
                self._images[animation][frame] = pg.transform.flip(image, True, False)
