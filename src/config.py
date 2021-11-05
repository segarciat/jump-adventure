"""Game configuration file specifying game constants and resource locations."""
import os


DEBUG = False
# Screen Settings.
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 840
TITLE = "Jump Adventure"
FPS = 60
MS_PER_UPDATE = 1.0 / FPS
MAP_FILE = 'test.tmx'

# Game directory and game assets directories.
GAME_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(GAME_DIR, 'assets', 'images')
SND_DIR = os.path.join(GAME_DIR, 'assets', 'sounds')
MAP_DIR = os.path.join(GAME_DIR, 'assets', 'maps')

# Color RGBs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TRANSPARENT = (255, 255, 255, 0)
COLOR_KEY = BLACK

# Sprite sheets.
SPRITE_SHEETS = (
    # {"img": "onlyObjects_default.png", "xml": "onlyObjects_default.xml"},  # Game Object images.
    {"img": "blueSheet.png", "xml": "blueSheet.xml"},  # UI images.
)

# Game font names.
FONT_NAMES = ('arial', 'calibri')

# Sprite Layers (smallest is topmost).
EFFECTS_LAYER = 5
ITEM_LAYER = 3


# Group names
DRAW_GROUP = "drawable"
UPDATE_GROUP = "updatable"
ITEMS_GROUP = "items"
OBSTACLE_GROUP = "obstacles"
PLATFORM_GROUP = "platforms"
STEPS_GROUP = "steps"
