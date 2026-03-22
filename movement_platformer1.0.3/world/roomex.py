import pygame

class Room:
    def __init__(self):
        self.platforms = [
            pygame.Rect(0,680,2000,40), #ground
            pygame.Rect(400,600,200,20),
            pygame.Rect(200,450,200,20),
            pygame.Rect(700,450,200,20),
            pygame.Rect(1100,350,200,20),
            pygame.Rect(0,500,20,500)
        ]
        self.enemies = []
        self.hazards = []

    def update(self, dt):
        pass

    def draw(self, screen, camera):
        for p in self.platforms:
            screen_rect = camera.apply(p)
            pygame.draw.rect(screen, (100,100,100), screen_rect)