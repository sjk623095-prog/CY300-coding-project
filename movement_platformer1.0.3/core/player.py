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
        accel = 4000  # tune this

        if keys[pygame.K_a]:
            self.body.vx -= accel * dt
        elif keys[pygame.K_d]:
            self.body.vx += accel * dt

        max_speed = 800

        if self.body.vx > max_speed:
            self.body.vx = max_speed
        elif self.body.vx < -max_speed:
            self.body.vx = -max_speed
        #elif keys[pygame.K_w] (CLIMBING??)

        #jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.body.vy = self.jump_force
            self.on_ground = False
        

    def draw(self, screen, camera):
        x, y = camera.apply_pos(self.body.x, self.body.y)
        pygame.draw.rect(screen, (100, 100, 255), (x, y, 20, 40))