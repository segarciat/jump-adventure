import src.config as cfg

import src.world.physics as physics
from src.world.items.item import Item
from src.world.base_sprite import DrawableSprite, IUpdatable
from src.world.components.physics import PhysicsComponent


class ChainedWeight(DrawableSprite, IUpdatable, Item):
    DAMAGE = 2

    # Todo: add to platform group so that collisions happen between player and weight?
    def __init__(self, x, y, player, groups):
        DrawableSprite.__init__(self, groups, default_image_name='weightChained.png', shared=True)
        IUpdatable.__init__(self, groups)
        Item.__init__(self, groups)
        groups[cfg.OBSTACLE_GROUP].add(self)

        # Allows us to remove from group when weight hits the ground.
        self._update_group = groups[cfg.UPDATE_GROUP]
        # todo: Utility function to convert topleft coordinate to bottom middle?
        self.rect.topleft = x, y
        # Weight object hit box.
        self.hit_rect = self.rect.copy()
        # todo: in copying it, does it not already set this?
        self.hit_rect.topleft = x, y

        # Chain from witch the ChainedWeight hangs; only aesthetic.
        self.chain_image = DrawableSprite.get_image('chain.png', shared=True)
        self.chain_rect = self.chain_image.get_rect()
        self.chain_rect.midtop = self.rect.midtop
        self.rect.midtop = self.chain_rect.midbottom

        # Weight cannot fall while chained
        self.physics = PhysicsComponent(
            sprite=self,
            x=x,
            y=y,
            forces=[physics.apply_gravity, physics.apply_gravity],
            collision_handlers=[
                {'callback': physics.halt_collide_y, 'colliders': groups[cfg.OBSTACLE_GROUP]},
                {'callback': physics.halt_collide_x, 'colliders': groups[cfg.OBSTACLE_GROUP]}
            ]
        )
        self.player = player
        self._chained = True

    def affect(self, player):
        if player.sprite.state != player.sprite.hurt_state and self.physics.vel.y > 0:
            player.sprite.hurt(half_heart_damage=ChainedWeight.DAMAGE)
            # todo: code knock-back code to rewrite.
            if player.sprite.physics.pos.x > self.rect.centerx:
                player.sprite.hit_rect.left = self.hit_rect.right
                player.sprite.physics.vel.xy = 300, -300
            else:
                player.sprite.hit_rect.right = self.hit_rect.left
                player.sprite.physics.vel.xy = -300, -300

    def activate(self):
        """Causes chain to break if the player is anywhere under it; only called once."""
        if self.player.sprite.rect.right > self.rect.left and self.player.sprite.rect.left < self.rect.right and self.player.sprite.rect.top > self.rect.bottom:
            hanging_point = self.rect.midtop
            self.image = DrawableSprite.get_image('weight.png', shared=True)
            self.rect = self.image.get_rect()
            self.rect.midtop = hanging_point
            self.hit_rect = self.rect
            self._chained = False

    def update(self, *args, **kwargs) -> None:
        """The weight falls as fast as gravity dictates, until it reaches the ground."""
        if self._chained:
            self.activate()
        else:
            # Purposely apply gravity twice.. have it drop very quickly.
            # todo: use physics component?
            self.physics.update()
            # todo: remove from 'updatable' group whe reach ground?
            # if self.vel.y == 0:
            #     self.update_group.remove(self)

    def draw(self, screen, camera):
        screen.blit(self.chain_image, camera.apply(self.chain_rect))
        screen.blit(self.image, camera.apply(self.rect))
