import os
import pytmx
import pygame as pg


import src.config as cfg
import src.world.physics as physics
from src.world.camera import Camera
from src.sprites.player import Player
from src.sprites.platform import Platform
from src.sprites.coin import Coin
from src.sprites.springboard import SpringBoard


class Level:
    """Class that creates, draws, and updates the game world, including the map and all sprites."""

    def __init__(self, filename: str):
        """Creates a maps and all level sprites from a given filename with pytmx extension."""
        self._groups = None
        self._player = None
        self._camera = None
        self._ai_mobs = []
        self._map_surface = None
        self._map_rect = None
        # Initialize all sprites in game world.
        tm = pytmx.util_pygame.load_pygame(os.path.join(cfg.MAP_DIR, filename), pixelalpha=True)
        self._make_map(tm)
        self._init_sprites(tm)

    def _make_map(self, tm: pytmx.TiledMap):
        """Creates a pygame Surface from the loaded TiledMap object."""
        surf = pg.Surface((tm.width * tm.tilewidth, tm.height * tm.tileheight))
        for layer in tm.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = tm.get_tile_image_by_gid(gid)
                    if tile:
                        surf.blit(tile, (x * tm.tilewidth, y * tm.tileheight))
        surf.set_colorkey(cfg.COLOR_KEY)
        if surf.get_alpha() is None:
            self._map_surface = surf.convert()
        else:
            self._map_surface = surf.convert_alpha()
        self._map_rect = self._map_surface.get_rect()

    def _init_sprites(self, tm: pytmx.TiledMap) -> None:
        """Initializes all of the pygame sprites from the object layers in the TiledMap object."""
        self._groups = {
            'all': pg.sprite.LayeredUpdates(),
            'platforms': pg.sprite.Group(),
            'steps': pg.sprite.Group(),
            'items': pg.sprite.Group(),
        }
        game_objects = {}
        # Expect a single player, and multiple of other entities.
        for t_obj in tm.objects:
            if t_obj.name == "player":
                game_objects[t_obj.name] = t_obj
            else:
                game_objects.setdefault(t_obj.name, []).append(t_obj)

        # Create the player and world camera.
        p = game_objects.get('player')
        self._player = Player(p.x, p.y, Player.P1, self._groups)
        self._camera = Camera(self._map_rect.width, self._map_rect.height, self._player)

        # Create all other spites.
        for p in game_objects.get("platform"):
            self._groups['platforms'].add(Platform(p.x, p.y, p.width, p.height, self._groups))
        for p in game_objects.get("step"):
            self._groups['steps'].add(Platform(p.x, p.y, p.width, p.height, self._groups))
        for p in game_objects.get("coin"):
            if p.coin_type == 'bronze':
                self._groups['items'].add(Coin.bronze(p.x, p.y, self._groups))
            elif p.coin_type == 'silver':
                self._groups['items'].add(Coin.silver(p.x, p.y, self._groups))
            elif p.coin_type == 'gold':
                self._groups['items'].add(Coin.gold(p.x, p.y, self._groups))

        for p in game_objects.get('springboard'):
            self._groups['items'].add(SpringBoard(p.x, p.y, self._groups))

    def process_inputs(self) -> None:
        """Handles keys and clicks that affect the game world."""
        self._player.handle_keys()
        # Convert mouse coordinates to world coordinates.
        # mouse_x, mouse_y = pg.mouse.get_pos()
        # mouse_world_pos = pg.math.Vector2(mouse_x + self._camera.rect.x, mouse_y + self._camera.rect.y)

    def update(self, dt: float) -> None:
        """Updates the game world's AI, sprites, camera, and resolves collisions.

        :param dt: time elapsed since the last update of the game world.
        :return: None
        """
        for ai in self._ai_mobs:
            ai.update(dt)
        self._groups['all'].update(dt)
        self._camera.update()

        # Resolve collisions.
        items = pg.sprite.spritecollide(self._player, self._groups['items'], dokill=False,
                                        collided=physics.collide_hit_rect)

        for item in items:
            item.activate(self._player)

    def draw(self, screen: pg.Surface) -> None:
        """Draws every sprite in the game world, as well as heads-up display elements.

        :param screen: The screen surface that the world's elements will be drawn to.
        :return: None
        """
        # Draw the map.
        screen.blit(self._map_surface, self._camera.apply(self._map_rect))
        # Draw all sprites.
        for sprite in self._groups['all']:
            screen.blit(sprite.image, self._camera.apply(sprite.rect))
            if cfg.DEBUG:
                pg.draw.rect(screen, (255, 255, 255), self._camera.apply(sprite.hit_rect), 1)
        self._player.hud.draw(screen)
