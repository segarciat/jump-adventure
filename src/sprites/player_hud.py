import src.config as cfg
import src.services.image_loader as image_loader


class PlayerHud:
    def __init__(self, player):
        # Player lives image.
        self.player = player
        self._hud_player = image_loader.get_image(f'hud_p{player.player_number}.png')
        self._hud_player_rect = self._hud_player.get_rect()
        self._hud_player_rect.topleft = (5, 5)

        # Times image for player lives.
        self._hud_x = image_loader.get_image('hud_x.png')
        self._x_lives_rect = self._hud_x.get_rect()
        self._x_lives_rect.midleft = (self._hud_player_rect.right + 5, self._hud_player_rect.centery)

        # Coin (HUD) image.
        self._hud_coins = image_loader.get_image('hud_coins.png')
        self._hud_coins_rect = self._hud_coins.get_rect()
        self._hud_coins_rect.topright = (cfg.SCREEN_WIDTH / 2, 5)

        # Times image for coin and lives count.
        self._x_coins_rect = self._x_lives_rect.copy()
        self._x_coins_rect.left = self._hud_coins_rect.right + 5
        self._hud_digits = [image_loader.get_image(f'hud_{i}.png') for i in range(0, 10)]

        # Heart images for health
        self._hud_heart_full = image_loader.get_image('hud_heartFull.png')
        self._hud_heart_half = image_loader.get_image('hud_heartHalf.png')

    def _draw_digits(self, screen, count, x, y):
        digits = []
        if count == 0:
            digits.append(0)
        while count > 0:
            digits.append(count % 10)
            count //= 10
        digits.reverse()

        for digit in digits:
            digit_surf = self._hud_digits[digit]
            digit_rect = digit_surf.get_rect()
            digit_rect.midleft = x, y
            screen.blit(digit_surf, digit_rect)
            x += digit_surf.get_width()

    def _draw_health(self, screen):
        heart_x = self._hud_player_rect.left
        for i in range(int(self.player.hearts)):
            screen.blit(self._hud_heart_full, (heart_x, self._hud_player_rect.bottom + 5))
            heart_x += self._hud_heart_full.get_width()
        if int(self.player.hearts) < self.player.hearts:
            screen.blit(self._hud_heart_half, (heart_x, self._hud_player_rect.bottom + 5))

    def draw(self, screen):
        screen.blit(self._hud_player, self._hud_player_rect)
        screen.blit(self._hud_x, self._x_lives_rect)
        screen.blit(self._hud_coins, self._hud_coins_rect)
        screen.blit(self._hud_x, self._x_coins_rect)

        self._draw_digits(screen, self.player.lives, self._x_lives_rect.right + 5, self._hud_player_rect.centery)
        self._draw_digits(screen, self.player.coins, self._x_coins_rect.right + 5, self._hud_coins_rect.centery)
        self._draw_health(screen)
