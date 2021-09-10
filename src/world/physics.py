"""Module that deals with resolving collisions between sprites."""
import pygame as pg

# Acceleration due to gravity.
_GRAVITY = 4000


def collide_hit_rect(sprite_a, sprite_b) -> bool:
    """ Determines whether the sprites' hit_rect rectangles overlap."""
    return sprite_a.hit_rect.colliderect(sprite_b.hit_rect)


def handle_platform_collision(sprite, displacement: pg.math.Vector2):
    """Uses the midbottom as the handle of collision for the sprite."""
    colliders = sprite.all_groups['platforms']

    # Collision in y direction.
    old_y = sprite.pos.y
    sprite.pos.y += int(displacement.y)
    sprite.hit_rect.bottom = sprite.pos.y
    collider = pg.sprite.spritecollideany(sprite, colliders, collide_hit_rect)
    if collider:
        # Sprite falls on top of platform.
        if old_y <= collider.hit_rect.top < sprite.hit_rect.bottom:
            sprite.pos.y = collider.hit_rect.top
            sprite.vel.y = 0
            sprite.acc.y = 0
        # Sprite hits platform from the bottom.
        elif (old_y - sprite.hit_rect.height) >= collider.hit_rect.bottom > sprite.hit_rect.top:
            sprite.pos.y = collider.hit_rect.bottom + sprite.hit_rect.height
            sprite.vel.y = 0
            sprite.acc.y = 0
        sprite.hit_rect.bottom = sprite.pos.y

    # Collision in x direction.
    old_x = sprite.pos.x
    sprite.pos.x += int(displacement.x)
    sprite.hit_rect.centerx = sprite.pos.x
    collider = pg.sprite.spritecollideany(sprite, colliders, collide_hit_rect)
    if collider:
        # Sprite runs into platform from the left.
        if (old_x + sprite.hit_rect.width / 2) <= collider.hit_rect.left < (sprite.pos.x + sprite.hit_rect.width / 2):
            sprite.pos.x = collider.hit_rect.left - sprite.hit_rect.width / 2
            sprite.acc.x = 0
            sprite.vel.x = 0
        # Sprite runs into platform from the right.
        elif old_x - sprite.hit_rect.width / 2 >= collider.hit_rect.right > sprite.pos.x - sprite.hit_rect.width / 2:
            sprite.pos.x = collider.hit_rect.right + sprite.hit_rect.width / 2
            sprite.acc.x = 0
            sprite.vel.x = 0
        sprite.hit_rect.centerx = sprite.pos.x

    sprite.rect.midbottom = sprite.pos


def handle_ladder_collision(sprite, displacement):
    colliders = sprite.all_groups['steps']
    steps = pg.sprite.spritecollide(sprite, colliders, False, collide_hit_rect)

    if steps:
        # Find the highest platform hit.
        highest = steps[0]
        for step in steps:
            if step.rect.y < highest.rect.y:
                highest = step
        # Plat sprite on top of that platform.
        if sprite.pos.y > highest.rect.y:
            sprite.pos.y = highest.rect.y
            sprite.vel.y = 0
            sprite.acc.y = 0

    sprite.hit_rect.midbottom = sprite.pos
    sprite.rect.midbottom = sprite.pos


def handle_ground_collision(sprite, displacement):
    handle_platform_collision(sprite, displacement)
    handle_ladder_collision(sprite, displacement)


def apply_gravity(sprite, dt: float) -> None:
    """Updates the sprite's velocity by accelerating it towards the ground."""
    sprite.vel.y += _GRAVITY * dt


def on_ground(sprite) -> bool:
    """Determines if the given sprite's collision rectangle is on top on the ground."""
    sprite.hit_rect.y += 1
    platforms = pg.sprite.spritecollideany(sprite, sprite.all_groups['platforms'], collide_hit_rect)
    steps = pg.sprite.spritecollideany(sprite, sprite.all_groups['steps'], collide_hit_rect)
    sprite.hit_rect.y -= 1
    return platforms is not None or steps is not None
