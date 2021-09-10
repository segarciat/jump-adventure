import os
import pygame as pg

import src.config as cfg


class Sound:
    """Class for handling all sounds in the game."""
    def __init__(self):
        """Loads all sounds and stores them."""
        # self._music = {}
        self._sfx = {}
        print("Loading all sounds...")
        for filename in os.listdir(cfg.SND_DIR):
            if filename.endswith(".wav"):
                filepath = os.path.join(cfg.SND_DIR, filename)
                self._sfx[filename] = pg.mixer.Sound(filepath)

    def get_sfx(self, filename: str) -> pg.mixer.Sound:
        return self._sfx[filename]

    def play_sfx(self, filename: str) -> None:
        """Plays a sound effect whose name is indicated by the provided filename."""
        self._sfx[filename].play()


# Global sound class.
_sound_loader = Sound()
# Interface methods for the global class.
play_sfx = _sound_loader.play_sfx
get_sfx = _sound_loader.get_sfx
