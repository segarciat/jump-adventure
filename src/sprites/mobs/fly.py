from src.sprites.animated_sprite import AnimatedSprite


class Fly(AnimatedSprite):
    FLUTTER = 0
    DEAD = 1

    def __init__(self, x, y, all_groups):
        frames = [
            {'animation_number': Fly.FLUTTER, 'image_names': ['flyFly1.png', 'flyFly2.png']},
            {'animation_number': Fly.DEAD, 'image_names': ['flyDead.png']},
        ]
        AnimatedSprite.__init__(self, frames, all_groups, all_groups['all'])
