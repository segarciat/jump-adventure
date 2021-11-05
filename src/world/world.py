import os
import pytmx
import pygame as pg

import src.config as cfg
import src.world.physics as physics
from src.entities.player import Player
from src.world.camera import Camera
from src.world.factory import Factory


class World:
    """Class that creates, draws, and updates the game world, including the map and all sprites."""

    def __init__(self, filename: str):
        """Creates a maps and all level sprites from a given filename with pytmx extension."""
        self._groups = None
        self._player = None
        self._camera = None
        self._map_surface = None
        self._map_rect = None
        # Initialize all sprites in game world.
        tm = pytmx.util_pygame.load_pygame(os.path.join(cfg.MAP_DIR, filename), pixelalpha=True)
        self._make_map(tm)
        self._init_sprites(tm)

    @property
    def groups(self) -> dict[str, pg.sprite.Group]:
        """Returns a dictionary of all sprite groups sprites in the game world belong to."""
        return self._groups

    @property
    def player(self):
        """Returns the sprite driven by the player."""
        return self._player

    def _make_map(self, tm: pytmx.TiledMap) -> None:
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
            cfg.DRAW_GROUP: pg.sprite.LayeredUpdates(),
            cfg.UPDATE_GROUP: pg.sprite.Group(),
            cfg.ITEMS_GROUP: pg.sprite.Group(),
            cfg.OBSTACLE_GROUP: pg.sprite.Group(),
            cfg.PLATFORM_GROUP: pg.sprite.Group(),
            cfg.STEPS_GROUP: pg.sprite.Group(),
        }
        p = tm.get_object_by_name("player")
        self._player = Player(Factory.create_alien(p, self._groups))
        self._camera = Camera(self._map_rect.width, self._map_rect.height, self._player.sprite)
        for p in tm.objects:
            Factory.create(p, self.player, self._groups)

    def update(self, *args, **kwargs) -> None:
        """Updates the game world's sprites, camera, and resolves collisions."""
        self._groups[cfg.UPDATE_GROUP].update(*args, **kwargs, world=self)
        self._camera.update()

        # Resolve collisions.
        items = pg.sprite.spritecollide(self._player.sprite, self._groups[cfg.ITEMS_GROUP], dokill=False,
                                        collided=physics.collide_hit_rect)
        for item in items:
            item.affect(self._player)

    def draw(self, screen: pg.Surface) -> None:
        """Draws every sprite in the game world, as well as heads-up display elements."""
        # Draw the map.
        screen.blit(self._map_surface, self._camera.apply(self._map_rect))
        # Draw all sprites.
        for sprite in self._groups[cfg.DRAW_GROUP]:
            sprite.draw(screen, self._camera)
        if cfg.DEBUG:
            for sprite in self._groups[cfg.DRAW_GROUP]:
                pg.draw.rect(screen, (255, 255, 255), self._camera.apply(sprite.hit_rect), 1)
            for sprite in self._groups[cfg.OBSTACLE_GROUP]:
                pg.draw.rect(screen, (255, 255, 255), self._camera.apply(sprite.hit_rect), 1)
            for sprite in self._groups[cfg.STEPS_GROUP]:
                pg.draw.rect(screen, (255, 255, 255), self._camera.apply(sprite.hit_rect), 1)
        self._player.hud.draw(screen)
