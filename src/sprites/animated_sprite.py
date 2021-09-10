import math
import typing
import pygame as pg

import src.config as cfg
import src.services.image_loader as image_loader
from src.sprites.base_sprite import BaseSprite


class AnimatedSprite(BaseSprite):
    """A BaseSprite that has at least one animation with multiple frames.

    Implementation based on the content in Chapter 2: 2D Graphics of Game Programming Algorithms and Techniques by
    Sanjay Madhav.
    """
    def __init__(self, frame_info, all_groups: typing.Dict[str, pg.sprite.Group], *groups: pg.sprite.Group):
        """

        :param images: List of all filenames used to animate this sprite.
        :param frame_info: List of dictionaries. Each dictionary has a 'start_frame' and a 'num_frames' key, one for
                           each animation for this sprite.
        :param all_groups: A dictionary of all the game world's sprite groups.
        :param groups: A possibly empty sequence of sprite groups that the sprite should be added to.
        """
        # Pass in default image to draw.
        BaseSprite.__init__(self, frame_info[0]['image_names'][0], all_groups, *groups)

        self._images = {}
        for anim in frame_info:
            animation_number, image_names = anim['animation_number'], anim['image_names']
            self._images[animation_number] = []
            for name in image_names:
                image = image_loader.get_image(name)
                image.set_colorkey(cfg.BLACK)
                self._images[animation_number].append(image)

        # Store animation data.
        self._anim_num = 0       # Animation index.
        self._current_frame = 0  # Frame number of current animation.
        self._frame_time = 0     # Amount of time in current frame.
        self._anim_fps = 24.0    # Animation frame rate.

        # Animation 0 is the default
        # self.change_anim(0)

    def change_anim(self, animation_number: int) -> None:
        """

        :param animation_number: Index of the animation in the frame_info list.
        :return: None
        """
        self._anim_num = animation_number
        self._current_frame = 0
        self._frame_time = 0.0
        self.image = self._images[animation_number][self._current_frame]

    def update_anim(self, dt: float) -> None:
        """Updates the current frame of animation.

        :param dt: Time elapsed since the sprite was last updated.
        :return: None
        """
        # Update time in current frame of the animation.
        self._frame_time += dt

        # Check if its time to update frame.
        if self._frame_time > (1 / self._anim_fps):
            self._current_frame += math.floor(self._frame_time * self._anim_fps)

            # Check if we reached final frame in animation.
            if self._current_frame >= len(self._images[self._anim_num]):
                self._handle_last_frame()
            # Update the active image
            self.image = self._images[self._anim_num][self._current_frame]
            self._frame_time = self._frame_time % (1 / self._anim_fps)

    # Subclasses might override to decide what to do at end of animation, like kill the sprite.
    def _handle_last_frame(self) -> None:
        """Handles the last frame of an animation; defaults to looping the animation."""
        self._current_frame = self._current_frame % len(self._images[self._anim_num])
