from src.sprites.animated_sprite import AnimatedSprite


class Poker(AnimatedSprite):
    MAD = 0
    SAD = 1

    def __init__(self, x, y, all_groups):
        frames = [
            {'animation_number': Poker.MAD, 'image_names': ['pokerMad.png']},
            {'animation_number': Poker.SAD, 'image_names': ['pokerSad.png']},
        ]
        AnimatedSprite.__init__(self, frames, all_groups, all_groups['all'])
