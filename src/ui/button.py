import typing
import pygame as pg

import src.services.text as text_renderer
import src.services.image_loader as image_loader
import src.input.input_manager as input_manager
from src.input.input_state import InputState

_BTN_IMAGES = ["blue_button04.png", "blue_button02.png", "blue_button03.png"]


class Button:
    """Represents a button sprite that, upon click, runs some action."""
    _HOVER_OFF, _HOVER_ON, _CLICKED = 0, 1, 2

    def __init__(self, action: typing.Callable, text: str, size: int, color):
        """Renders text onto the button and assigns the action.

        :param action: Function to run when button is clicked.
        :param text: Text to be rendered on the button.
        :param size: Size of the font for the text to be rendered.
        :param color: Color for the text to be rendered.
        """
        self._images = {
            Button._HOVER_OFF: image_loader.get_image("blue_button04.png"),
            Button._HOVER_ON: image_loader.get_image("blue_button02.png"),
            Button._CLICKED: image_loader.get_image("blue_button03.png")
        }
        # Add text to buttons.
        for image in self._images.values():
            text_renderer.render(image, text, size, color)
        self.image = self._images[Button._HOVER_OFF]
        self.rect = self.image.get_rect()
        self._action = action

    def handle_mouse(self):
        """Either animates the button or executes the function that it encapsulates."""
        # Keep track of bottom of button.
        old_bot = self.rect.bottomleft
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_state = input_manager.mouse_state[InputState.MOUSE_LEFT]
        if self._is_hovering(mouse_x, mouse_y):
            self.image = self._images[Button._HOVER_OFF]
            if mouse_state == InputState.STILL_PRESSED:
                self.image = self._images[Button._CLICKED]
            elif mouse_state == InputState.JUST_RELEASED:
                # toggle-off clicked animation
                self._action()
        else:
            self.image = self._images[Button._HOVER_OFF]
        # Update button position
        self.rect = self.image.get_rect()
        self.rect.bottomleft = old_bot

    def _is_hovering(self, mouse_x: int, mouse_y: int):
        """Determines whether the mouse is hovering over the button sprite."""
        if mouse_x < self.rect.left:
            return False
        if mouse_x > self.rect.right:
            return False
        if mouse_y < self.rect.top:
            return False
        if mouse_y > self.rect.bottom:
            return False
        return True
