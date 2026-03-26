import pygame
from physics.physics_body import PhysicsBody1
from core.state_machine import (
    StateMachine,
    IdleState,
    RunState,
    JumpState,
    FallState
)


class Player:
    def __init__(self, x,y):
        self.jump_pressed_last = False
        self.max_jumps = 2
        self.jump_count = 0
        self.on_wall = False
        self.wall_dir = None
        self.body = PhysicsBody1(x,y)
        self.state_machine = StateMachine(IdleState())

        self.speed = 600
        self.jump_force = -900
        self.on_ground = False
    
    def update(self, dt):

        
        keys = pygame.key.get_pressed()

        #horizontal movement
        accel = 3000
        friction = 2000
        max_speed = 800

        move_input = 0
        if keys[pygame.K_a]:
            move_input = -1
        elif keys[pygame.K_d]:
            move_input = 1

        # --- Apply acceleration ---
        self.body.vx += move_input * accel * dt

        # --- Apply friction ONLY when grounded and no input ---
        if move_input == 0 and self.on_ground:
            if self.body.vx > 0:
                self.body.vx -= friction * dt
                if self.body.vx < 0:
                    self.body.vx = 0
            elif self.body.vx < 0:
                self.body.vx += friction * dt
                if self.body.vx > 0:
                    self.body.vx = 0

        # --- Clamp speed ---
        self.body.vx = max(-max_speed, min(max_speed, self.body.vx))
                #elif keys[pygame.K_w] (CLIMBING??)

        #jump/wj
        if keys[pygame.K_SPACE] and not self.jump_pressed_last:

            # --- NORMAL / DOUBLE JUMP ---
            if self.jump_count < self.max_jumps:
                self.body.vy = self.jump_force
                self.jump_count += 1
                self.state_machine.change(JumpState())

            # --- WALL JUMP ---
            elif self.on_wall:
                self.body.vy = self.jump_force

                if self.wall_dir == "left":
                    self.body.vx = 600
                elif self.wall_dir == "right":
                    self.body.vx = -600

                self.state_machine.change(JumpState())
        # --- Reset jumps when grounded ---
        if self.on_ground:
            self.jump_count = 0

        # --- Update state machine EVERY frame ---
        self.state_machine.update(self, dt)

        # --- Track jump input EVERY frame ---
        self.jump_pressed_last = keys[pygame.K_SPACE]


        

    def draw(self, screen, camera):
        x, y = camera.apply_pos(self.body.x, self.body.y)
        pygame.draw.rect(screen, (100, 100, 255), (x, y, 20, 40))