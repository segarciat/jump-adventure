import abc
import pygame as pg

import src.config as cfg
import src.input.input_manager as input_manager
from src.world.world import World
from src.utils.timer import Timer
from src.state import IState


class GameState(IState, metaclass=abc.ABCMeta):
    """Abstract class representing the state of the Game class."""
    def __init__(self, game):
        """Creates a GameState object to dive the behavior of the main object of class Game."""
        self._game = game

    def process_inputs(self) -> None:
        """Fetches any inputs in the queue since last frame and processes them."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._game.quit()
        input_manager.update_inputs()
        self._game.ui.process_inputs()

    def update(self, *args, **kwargs) -> None:
        """Updates the Game while in the current state."""
        pass

    @abc.abstractmethod
    def draw(self, screen: pg.Surface) -> None:
        pass

    def _transition(self, state: 'GameState') -> None:
        """Sets the state attribute of the object of class Game; created for use in lambda expressions."""
        self._game.state = state


class GameMainMenuState(GameState):
    """Main menu behavior for the Game class."""
    def __init__(self, game):
        """Creates the splash image for the main menu."""
        GameState.__init__(self, game)
        self._menu_splash = pg.Surface((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))

    def enter(self) -> None:
        """Clears the UI and makes the main menu available."""
        self._game.ui.clear()
        buttons = [
            {'action': lambda: self._transition(self._game.play_state), 'text': 'Play', 'size': 16, 'color': cfg.WHITE},
            {'action': self._game.quit, 'text': 'Exit', 'size': 16, 'color': cfg.WHITE},
        ]
        self._game.ui.make_menu("Main Menu", 24, cfg.WHITE, buttons)

    def draw(self, screen: pg.Surface) -> None:
        """Draws the game splash and the menu on top of it."""
        screen.blit(self._menu_splash, self._menu_splash.get_rect())
        self._game.ui.draw(screen)


class GamePlayingState(GameState):
    """Controls the main in-game (gameplay) behavior of the Game class."""
    def __init__(self, game):
        GameState.__init__(self, game)
        self._world = None
        self._paused = False

    def enter(self) -> None:
        """Clears the UI and creates the game world."""
        # Clear the UI.
        self._game.ui.clear()
        Timer.clear_timers()
        # TODO: Instead of hard-coding map file, allow user to select map from MainMenu, and play state passes that in.
        self._world = World(cfg.MAP_FILE)
        self._paused = False

    def process_inputs(self) -> None:
        """Processes key and mouse input queued since the last frame."""
        super().process_inputs()
        if input_manager.process_active_binding("pause"):
            self._toggle_pause()
        if not self._paused:
            self._world.player.process_inputs()

    def update(self, *args, **kwargs) -> None:
        """Updates the state of the game world to account for the elapsed time dt and determines if game is over."""
        if not self._paused:
            self._world.update()

    def draw(self, screen: pg.Surface) -> None:
        """Draws the game's world and UI onto the screen surface."""
        if not self._paused:
            screen.fill(cfg.WHITE)
            self._world.draw(screen)
        self._game.ui.draw(screen)

    def _toggle_pause(self) -> None:
        """Toggles the pause mode of the game."""
        if self._paused:
            self._game.ui.pop_menu()
            Timer.unpause_timers()
        else:
            buttons = [
                {'action': self._toggle_pause, 'text': 'Resume', 'size': 16, 'color': cfg.WHITE},
                {'action': self.enter, 'text': 'Restart', 'size': 16, 'color': cfg.WHITE},
                {
                    'action': lambda: self._transition(self._game.main_menu_state),
                    'text': 'Main Menu',
                    'size': 16,
                    'color': cfg.WHITE,
                 },
            ]
            self._game.ui.make_menu("Game Paused", 24, cfg.WHITE, buttons)
            Timer.pause_timers()
        self._paused = not self._paused
