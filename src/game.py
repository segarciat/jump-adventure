import sys
import pygame as pg

import src.config as cfg
# Loads all sprite sheet images and sounds upon import.
import src.services.image_loader
import src.services.sound
from src.state import StatefulMixin
from src.game_state import GamePlayingState, GameMainMenuState
from src.ui.ui import UI


class Game(StatefulMixin):
    """Top-level game class for running the current pygame application."""
    def __init__(self):
        """Sets the game screen and clock."""
        StatefulMixin.__init__(self)
        self._screen = pg.display.get_surface()
        self._clock = pg.time.Clock()
        self._ui = UI()
        self._running = False

        self._play_state = GamePlayingState(self)
        self._main_menu_state = GameMainMenuState(self)
        self._state = self._main_menu_state
        self._state.enter()

    @property
    def play_state(self) -> GamePlayingState:
        """Returns Game object's GamePlayingState attribute, which drives the main gameplay behavior."""
        return self._play_state

    @property
    def main_menu_state(self) -> GameMainMenuState:
        """Returns Game object's GameMainMenuState attribute, which drives the main menu behavior."""
        return self._main_menu_state

    @property
    def ui(self) -> UI:
        """Returns Game object's UI object, which handles user interface elements."""
        return self._ui

    def run(self) -> None:
        """Runs the game loop: processes inputs, updates, and draws at a frame rate specified in a config file."""
        self._running = True
        while self._running:
            self._clock.tick(cfg.FPS) / 1000
            self._state.process_inputs()
            self._state.update()
            self._state.draw(self._screen)
            pg.display.set_caption(f"{cfg.TITLE}: {int(self._clock.get_fps())} (FPS)")
            pg.display.flip()

    def quit(self) -> None:
        sys.exit()
