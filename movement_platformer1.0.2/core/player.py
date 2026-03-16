import pygame
from physics.physics_body import PhysicsBody1


class Player:
    def __init__(self, x,y):
        self.body = PhysicsBody1(x,y)

        self.speed = 600
        self.jump_force = -900
        self.on_ground = False
    
    def update(self, dt):
        
        keys = pygame.key.get_pressed()

        #horizontal movement
        if keys[pygame.K_a]:
            self.body.vx = -self.speed
        elif keys[pygame.K_d]:
            self.body.vx = +self.speed
        else:
            self.body.vx = 0
        #elif keys[pygame.K_w] (CLIMBING??)

        #jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.body.vy = self.jump_force
            self.on_ground = False
        
        #physics
        self.body.apply_gravity()
        self.body.integrate(dt)

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 255), (self.body.x, self.body.y, 20, 40))