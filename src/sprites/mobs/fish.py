from src.sprites.animated_sprite import AnimatedSprite


class Fish(AnimatedSprite):
    SWIM = 0
    DEAD = 1

    def __init__(self, x, y, all_groups):
        frames = [
            {'animation_number': Fish.SWIM, 'image_names': ['fishSwim1.png', 'fishSwim2.png']},
            {'animation_number': Fish.DEAD, 'image_names': ['fishDead.png']},
        ]
        AnimatedSprite.__init__(self, frames, all_groups, all_groups['all'])
