"""Module that deals with resolving collisions between sprites."""
import pygame as pg

import src.config as cfg


# Acceleration due to gravity.
_GRAVITY = 4000


def collide_hit_rect(sprite_a, sprite_b) -> bool:
    """ Determines whether the sprites' hit_rect rectangles overlap."""
    return sprite_a.hit_rect.colliderect(sprite_b.hit_rect)


def halt_collide_x(sprite, obstacles: pg.sprite.Group, displacement: pg.math.Vector2) -> None:
    """Brings sprite to a halt when its displacement in the x-direction causes to hit one of the colliders.
    Stops the sprite from moving and positions its rectangle adjacent to the rectangle of the collider.
    
    :param sprite: DrawableSprite object with a physics component.
    :param obstacles: Sprite objects belonging to the 'obstacle' sprite group.
    :param displacement: 2D vector representing the displacement of sprite in the current frame.
    :return: None
    """
    obstacle = pg.sprite.spritecollideany(sprite, obstacles, collide_hit_rect)
    if obstacle and obstacle != sprite:
        # Sprite runs into platform from the left.
        if sprite.hit_rect.right > obstacle.hit_rect.left > sprite.hit_rect.right - displacement.x:
            sprite.hit_rect.right = obstacle.hit_rect.left
            sprite.physics.acc.x = 0
            sprite.physics.vel.x = 0
        # Sprite runs into platform from the right.
        elif sprite.hit_rect.left < obstacle.hit_rect.right < sprite.hit_rect.left - displacement.x:
            sprite.hit_rect.left = obstacle.hit_rect.right
            sprite.physics.acc.x = 0
            sprite.physics.vel.x = 0
    sprite.physics.pos.x = sprite.rect.centerx = sprite.hit_rect.centerx


def halt_collide_y(sprite, obstacles: pg.sprite.Group, displacement: pg.math.Vector2) -> None:
    """Brings sprite to a halt when its displacement in the y-direction causes to hit one of the colliders.
    Stops the sprite from moving and positions its rectangle adjacent to the rectangle of the collider.

        :param sprite: DrawableSprite object with a physics component.
        :param obstacles: Sprite Group consisting of obstacles that sprite may run into.
        :param displacement: 2D vector representing the displacement of sprite in the current frame.
        :return: None
        """
    obstacle = pg.sprite.spritecollideany(sprite, obstacles, collide_hit_rect)
    if obstacle and obstacle != sprite:
        # Sprite falls on top of platform.
        if sprite.hit_rect.bottom - displacement.y < obstacle.hit_rect.top < sprite.hit_rect.bottom:
            sprite.hit_rect.bottom = obstacle.hit_rect.top
            sprite.physics.vel.y = 0
            sprite.physics.acc.y = 0
        # Sprite hits platform from the bottom.
        elif sprite.hit_rect.top - displacement.y > obstacle.hit_rect.bottom > sprite.hit_rect.top:
            sprite.hit_rect.top = obstacle.hit_rect.bottom
            sprite.physics.vel.y = 0
            sprite.physics.acc.y = 0
    sprite.physics.pos.y = sprite.rect.bottom = sprite.hit_rect.bottom


def step_collision(sprite, steps: pg.sprite.Group, displacement:pg.math.Vector2):
    """

    :param sprite: Sprite object walking along a slope made up of steps.
    :param steps: Sprite group representing the steps used to ascend or descend a slope in the game world.
    :param displacement: 2D vector representing the displacement of the sprite.
    :return:
    """
    sprite.hit_rect.midbottom = sprite.physics.pos.xy
    steps = pg.sprite.spritecollide(sprite, steps, False, collide_hit_rect)

    if steps:
        # Find the highest platform hit.
        highest = steps[0]
        for step in steps:
            if step.hit_rect.y < highest.hit_rect.y:
                highest = step
        # Plat sprite on top of that platform.
        if sprite.physics.pos.y > highest.hit_rect.y:
            sprite.physics.pos.y = highest.hit_rect.y
            sprite.physics.vel.y = 0
            sprite.physics.acc.y = 0

    sprite.hit_rect.midbottom = sprite.rect.midbottom = sprite.physics.pos


def on_ground(sprite, world) -> bool:
    """Determines if the given sprite's collision rectangle is on top on the ground."""
    sprite.hit_rect.y += 1
    steps = pg.sprite.spritecollideany(sprite, world.groups[cfg.STEPS_GROUP], collide_hit_rect)
    obstacles = pg.sprite.spritecollideany(sprite, world.groups[cfg.OBSTACLE_GROUP], collide_hit_rect)
    sprite.hit_rect.y -= 1
    return steps is not None or obstacles is not None


def apply_gravity(pos, vel, acc) -> None:
    """Updates the sprite's velocity by accelerating it towards the ground."""
    vel.y += _GRAVITY * cfg.MS_PER_UPDATE
