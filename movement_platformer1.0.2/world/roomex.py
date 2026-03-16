import pygame

class Room:
    def __init__(self):
        self.platforms = [
            pygame.Rect(0,680,2000,40), #ground
            pygame.Rect(400,550,200,20),
            pygame.Rect(400,450,200,20),
            pygame.Rect(700,450,200,20),
            pygame.Rect(1100,350,200,20),
        ]
        self.enemies = []
        self.hazards = []

    def update(self, dt):
        pass

    def draw(self, screen):
        for p in self.platforms:
            pygame.draw.rect(screen, (100,100,100), p)