import src.world.physics as physics
from src.sprites.items.base_item import BaseItem
from src.sprites.base_sprite import BaseSprite
from src.sprites.attributes.movable import MoveMixin


class ChainedWeight(BaseSprite, BaseItem, MoveMixin):
    DAMAGE = 2

    def __init__(self, x, y, player, all_groups):
        BaseSprite.__init__(self, 'weightChained.png', all_groups, all_groups['all'], all_groups['platforms'])
        BaseItem.__init__(self)
        MoveMixin.__init__(self, x, y)
        self.rect.topleft = x, y
        self.hit_rect.topleft = x, y
        self.chain_image = BaseSprite.get_image('chain.png')
        self.chain_rect = self.chain_image.get_rect()
        self.chain_rect.midtop = self.rect.midtop
        self.rect.midtop = self.chain_rect.midbottom
        self.pos.xy = self.rect.midbottom
        self.vel.xy = 0, 0
        self.player = player
        self.active = False

    def activate(self):
        if self.player.rect.right > self.rect.left and self.player.rect.left < self.rect.right:
            old_center = self.rect.center
            self.image = BaseSprite.get_image('weight.png')
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            self.active = True

    def collide(self, player):
        if player.state != player.hurt_state and self.vel.y > 0:
            player.hurt(half_heart_damage=ChainedWeight.DAMAGE)
            if player.pos.x > self.rect.centerx:
                player.vel.xy = 300, -300
            else:
                player.vel.xy = -300, -300

    def update(self, dt) -> None:
        """The weight falls as fast as gravity dictates, until it reaches the ground."""
        if self.active:
            # Purposely apply gravity twice.. have it drop very quickly.
            physics.apply_gravity(self, dt)
            physics.apply_gravity(self, dt)
            self.move(dt, physics.handle_ground_collision)
        elif not self.active:
            self.activate()

    def draw(self, screen, camera):
        screen.blit(self.chain_image, camera.apply(self.chain_rect))
        screen.blit(self.image, camera.apply(self.rect))
