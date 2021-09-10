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

        # Times image for coin count.
        self._x_coins_rect = self._x_lives_rect.copy()
        self._x_coins_rect.left = self._hud_coins_rect.right + 5
        self._hud_digits = [image_loader.get_image(f'hud_{i}.png') for i in range(0, 10)]

    def draw(self, screen):
        screen.blit(self._hud_player, self._hud_player_rect)
        screen.blit(self._hud_x, self._x_lives_rect)
        screen.blit(self._hud_coins, self._hud_coins_rect)
        screen.blit(self._hud_x, self._x_coins_rect)

        # Draw coin count.
        coins = self.player.coins

        # Calculate digits of coin count.
        digits = []
        if coins == 0:
            digits.append(0)
        while coins > 0:
            digits.append(coins % 10)
            coins //= 10
        digits.reverse()

        # Draw digits.
        digit_x = self._x_coins_rect.right + 5
        for digit in digits:
            digit_surf = self._hud_digits[digit]
            digit_rect = digit_surf.get_rect()
            digit_rect.midleft = digit_x, self._hud_coins_rect.centery
            screen.blit(digit_surf, digit_rect)
            digit_x += digit_surf.get_width()
