import pygame
from physics.physics_body import PhysicsBody1
from core.state_machine import (
    StateMachine,
    IdleState,
    RunState,
    JumpState,
    FallState
)

DASH_SPEED        = 1400   # px/s override during dash
DASH_DURATION     = 0.18   # seconds the dash velocity is held
DASH_COOLDOWN     = 0.8    # seconds before dash can be used again
LEVITATE_FALL_CAP = 150    # max fall speed (px/s) while levitating
LEVITATE_COOLDOWN = 1.2    # seconds before levitate can be used again


class Player:
    def __init__(self, x, y):
        self.jump_pressed_last = False
        self.max_jumps = 2
        self.jump_count = 0
        self.on_wall = False
        self.wall_dir = None
        self.body = PhysicsBody1(x, y)
        self.state_machine = StateMachine(IdleState())

        self.speed = 600
        self.jump_force = -900
        self.on_ground = False

        # --- Unlockable skills ---
        self.has_dash = False
        self.has_levitate = False

        # Dash state
        self.facing_dir = 1          # 1 = right, -1 = left
        self.is_dashing = False
        self.dash_timer = 0.0
        self.dash_cooldown_timer = 0.0
        self.dash_pressed_last = False

        # Levitate state
        self.levitate_cooldown_timer = 0.0
        self.levitate_pressed_last = False

        self.invincibility_timer = 0.0

    def take_damage(self):
        if self.invincibility_timer > 0:
            return False
        self.invincibility_timer = 1.0
        return True

    def update(self, dt):
        if self.invincibility_timer > 0:
            self.invincibility_timer -= dt

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        lmb = mouse[0]
        rmb = mouse[2]

        # Track facing direction from movement input
        if keys[pygame.K_d]:
            self.facing_dir = 1
        elif keys[pygame.K_a]:
            self.facing_dir = -1

        # --- Skill cooldown timers ---
        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= dt
        if self.dash_timer > 0:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.is_dashing = False
        if self.levitate_cooldown_timer > 0:
            self.levitate_cooldown_timer -= dt

        # --- DASH (RMB) ---
        if (self.has_dash
                and rmb
                and not self.dash_pressed_last
                and self.dash_cooldown_timer <= 0):
            self.is_dashing = True
            self.dash_timer = DASH_DURATION
            self.dash_cooldown_timer = DASH_COOLDOWN

        # --- LEVITATE (LMB) ---
        if self.has_levitate:
            if lmb and not self.levitate_pressed_last and not self.on_ground:
                if self.levitate_cooldown_timer <= 0:
                    self.jump_count = 0          # replenish jumps
                    self.levitate_cooldown_timer = LEVITATE_COOLDOWN
            # Slow falling while button held and airborne
            if lmb and not self.on_ground and self.body.vy > LEVITATE_FALL_CAP:
                self.body.vy = LEVITATE_FALL_CAP

        # --- Horizontal movement ---
        accel = 3000
        friction = 4000
        max_speed = 800

        move_input = 0
        if keys[pygame.K_a]:
            move_input = -1
        elif keys[pygame.K_d]:
            move_input = 1

        if self.is_dashing:
            # Override horizontal velocity for dash duration
            self.body.vx = self.facing_dir * DASH_SPEED
        else:
            self.body.vx += move_input * accel * dt

            if move_input == 0 and self.on_ground:
                if self.body.vx > 0:
                    self.body.vx -= friction * dt
                    if self.body.vx < 0:
                        self.body.vx = 0
                elif self.body.vx < 0:
                    self.body.vx += friction * dt
                    if self.body.vx > 0:
                        self.body.vx = 0

            self.body.vx = max(-max_speed, min(max_speed, self.body.vx))

        # --- Jump / wall jump ---
        if keys[pygame.K_SPACE] and not self.jump_pressed_last:

            if self.jump_count < self.max_jumps:
                self.body.vy = self.jump_force
                self.jump_count += 1
                self.state_machine.change(JumpState())

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

        # --- Track input state EVERY frame ---
        self.jump_pressed_last = keys[pygame.K_SPACE]
        self.dash_pressed_last = rmb
        self.levitate_pressed_last = lmb

    def draw(self, screen, camera):
        x, y = camera.apply_pos(self.body.x, self.body.y)
        pygame.draw.rect(screen, (100, 100, 255), (x, y, 20, 40))
