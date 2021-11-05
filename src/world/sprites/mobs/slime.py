from src.world.sprites import AnimatedSprite


class Slime(AnimatedSprite):
    WALK = 0
    DEAD = 1

    def __init__(self, x, y, all_groups):
        frames = [
            {'animation_number': Slime.WALK, 'image_names': ['slimeWalk1.png', 'slimeWalk2.png']},
            {'animation_number': Slime.DEAD, 'image_names': ['slimeDead.png']},
        ]
        AnimatedSprite.__init__(self, frames, all_groups, all_groups['all'])
