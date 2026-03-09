import pygame
from physics.physics_body import PhysicsBody1


class Player:
    def __init__(self, x,y):
        self.body = PhysicsBody1(x,y)
    
    def update(self, dt):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 255), (self.body.x, self.body.y, 20, 40))