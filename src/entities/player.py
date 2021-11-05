import src.input.input_manager as input_manager

from src.entities.player_hud import PlayerHUD


class Player:
    def __init__(self, sprite):
        self.lives = 1
        self.coins = 0
        self.sprite = sprite
        self._hud = PlayerHUD(self)

    @property
    def hud(self):
        return self._hud

    def process_inputs(self):
        if self.sprite.state == self.sprite.stand_state:
            # if just pressed right or just pressed left... walk,
            if input_manager.process_active_binding("right"):
                self.sprite.facing_left = False
                self.sprite.state = self.sprite.walk_state
            elif input_manager.process_active_binding("left"):
                self.sprite.facing_left = True
                self.sprite.state = self.sprite.walk_state
            elif input_manager.process_active_binding("duck"):
                self.sprite.state = self.sprite.duck_state
            elif input_manager.process_active_binding("jump"):
                self.sprite.state = self.sprite.jump_state
        elif self.sprite.state == self.sprite.duck_state:
            # if just released down (or... if not "still pressed"), stand
            if not input_manager.process_active_binding("duck"):
                self.sprite.state = self.sprite.stand_state
        elif self.sprite.state == self.sprite.walk_state:
            if not self.sprite.facing_left and not input_manager.process_active_binding("right") or \
                    self.sprite.facing_left and not input_manager.process_active_binding("left"):
                self.sprite.state = self.sprite.stand_state
            elif input_manager.process_active_binding("jump"):
                self.sprite.state = self.sprite.jump_state
        elif self.sprite.state == self.sprite.jump_state:
            pass


# jump stuff
"""def handle_keys(self):
    if self._alien.facing_left and input_manager.process_active_binding("right"):
        self._alien.facing_left = False
        self._alien.change_anim(self._alien.JUMP_R)
        # self._alien.physics.vel.x += abs(self._alien.physics.vel.x) / 2
    elif not self._alien.facing_left and input_manager.process_active_binding("left"):
        self._alien.facing_left = True
        self._alien.change_anim(self._alien.JUMP_L)
        # self._alien.physics.vel.x -= abs(self._alien.physics.vel.x) / 2"""