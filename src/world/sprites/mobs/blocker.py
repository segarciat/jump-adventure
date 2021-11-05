from src.sprites.animated_sprite import AnimatedSprite


class Blocker(AnimatedSprite):
    MAD = 0
    SAD = 1

    def __init__(self, x, y, all_groups):
        frames = [
            {'animation_number': Blocker.MAD, 'image_names': ['blockerMad.png']},
            {'animation_number': Blocker.SAD, 'image_names': ['blockerSad.png']},
        ]
        AnimatedSprite.__init__(self, frames, all_groups, all_groups['all'])
