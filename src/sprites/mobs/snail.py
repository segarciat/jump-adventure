from src.sprites.animated_sprite import AnimatedSprite


class Snail(AnimatedSprite):
    SHELL = 0
    WALK = 1
    SHELL_UPSIDE_DOWN = 2

    def __init__(self, x, y, all_groups):
        frames = [
            {'animation_number': Snail.SHELL, 'image_names': ['snailShell.png']},
            {'animation_number': Snail.WALK, 'image_names': ['snailWalk1.png', 'snailWalk2.png']},
            {'animation_number': Snail.SHELL_UPSIDE_DOWN, 'image_names': ['snailShell_upside_down.png']},
        ]
        AnimatedSprite.__init__(self, frames, all_groups, all_groups['all'])
