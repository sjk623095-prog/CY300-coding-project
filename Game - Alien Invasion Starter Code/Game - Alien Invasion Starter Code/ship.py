import pygame

class Ship:
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        # Load the ship image and get its rect.
        self.image = pygame.image.load('Game - Alien Invasion Starter Code\Game - Alien Invasion Starter Code\images\ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        #Store a float for the ships exact horizontal position
        self.x = float(self.rect.x)

        #Movement flags starting with a ship thats not moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update te ships position based on the movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed #increase this number to move faster
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x


    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)