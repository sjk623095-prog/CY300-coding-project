import pygame
import math
from physics.physics_body import PhysicsBody1
from settings import GRAVITY


class EnemyStateMachine:
    def __init__(self, initial_state):
        self.current = initial_state
        self.current.enter()

    def change(self, new_state):
        self.current.exit()
        self.current = new_state
        self.current.enter()

    def update(self, enemy, player, platforms, dt):
        self.current.update(enemy, player, platforms, dt)


class EnemyState:
    def enter(self): pass
    def exit(self): pass
    def update(self, enemy, player, platforms, dt): pass


# --- PatrolEnemy States ---

class PatrolState(EnemyState):
    def update(self, enemy, player, platforms, dt):
        if enemy._player_dist(player) < enemy.detection_range:
            enemy.state_machine.change(ChaseGroundState())
            return

        direction = 1 if enemy.body.vx >= 0 else -1

        if enemy.on_wall:
            enemy.body.vx = -PatrolEnemy.PATROL_SPEED * direction
            return

        if enemy.on_ground and not enemy._has_ground_ahead(platforms, direction):
            direction = -direction

        enemy.body.vx = PatrolEnemy.PATROL_SPEED * direction


class ChaseGroundState(EnemyState):
    def update(self, enemy, player, platforms, dt):
        direction = 1 if player.body.x > enemy.body.x else -1
        enemy.body.vx = PatrolEnemy.CHASE_SPEED * direction


# --- FlyingEnemy States ---

class HoverState(EnemyState):
    def update(self, enemy, player, platforms, dt):
        if enemy._player_dist(player) < enemy.detection_range:
            enemy.state_machine.change(ChaseAirState())
            return

        enemy.body.vx = 0
        enemy.body.vy = math.sin(enemy.hover_timer * 2.5) * FlyingEnemy.HOVER_AMP


class ChaseAirState(EnemyState):
    def update(self, enemy, player, platforms, dt):
        dx = player.body.x - enemy.body.x
        dy = player.body.y - enemy.body.y
        length = max((dx * dx + dy * dy) ** 0.5, 1)
        enemy.body.vx = (dx / length) * FlyingEnemy.CHASE_SPEED
        enemy.body.vy = (dy / length) * FlyingEnemy.CHASE_SPEED


# --- Base Class ---

class EnemyBase:
    WIDTH = 24
    HEIGHT = 40

    def __init__(self, x, y, detection_range=300):
        self.body = PhysicsBody1(x, y)
        self.detection_range = detection_range
        self.on_ground = False
        self.on_wall = False
        self.wall_dir = None
        self.state_machine = None

    def _player_dist(self, player):
        dx = player.body.x - self.body.x
        dy = player.body.y - self.body.y
        return (dx * dx + dy * dy) ** 0.5

    def _resolve_x(self, platforms):
        rect = pygame.Rect(self.body.x, self.body.y, self.WIDTH, self.HEIGHT)
        self.on_wall = False
        for p in platforms:
            if rect.colliderect(p):
                if self.body.vx > 0:
                    self.body.x = p.left - self.WIDTH
                    self.wall_dir = "right"
                elif self.body.vx < 0:
                    self.body.x = p.right
                    self.wall_dir = "left"
                self.body.vx = 0
                self.on_wall = True
                rect.x = self.body.x

    def _resolve_y(self, platforms):
        rect = pygame.Rect(self.body.x, self.body.y, self.WIDTH, self.HEIGHT)
        self.on_ground = False
        for p in platforms:
            if rect.colliderect(p):
                if self.body.vy >= 0:
                    self.body.y = p.top - self.HEIGHT
                    self.on_ground = True
                else:
                    self.body.y = p.bottom
                self.body.vy = 0
                rect.y = self.body.y

    def touches_hazard(self, hazards):
        rect = pygame.Rect(self.body.x, self.body.y, self.WIDTH, self.HEIGHT)
        return any(rect.colliderect(h) for h in hazards)

    def touches_player(self, player):
        rect = pygame.Rect(self.body.x, self.body.y, self.WIDTH, self.HEIGHT)
        player_rect = pygame.Rect(player.body.x, player.body.y, 20, 40)
        return rect.colliderect(player_rect)

    def update(self, dt, player, platforms):
        raise NotImplementedError

    def draw(self, screen, camera):
        raise NotImplementedError


# --- PatrolEnemy ---

class PatrolEnemy(EnemyBase):
    WIDTH = 24
    HEIGHT = 40
    PATROL_SPEED = 120
    CHASE_SPEED = 220

    def __init__(self, x, y, detection_range=300):
        super().__init__(x, y, detection_range)
        self.body.vx = self.PATROL_SPEED
        self.state_machine = EnemyStateMachine(PatrolState())

    def _has_ground_ahead(self, platforms, direction):
        check_x = (self.body.x + self.WIDTH + 4) if direction > 0 else (self.body.x - 4)
        check_y = self.body.y + self.HEIGHT + 4
        probe = pygame.Rect(check_x, check_y, 4, 4)
        return any(probe.colliderect(p) for p in platforms)

    def update(self, dt, player, platforms):
        self.body.vy += GRAVITY * dt
        self.body.vy = min(self.body.vy, self.body.max_fall_speed)

        self.state_machine.update(self, player, platforms, dt)

        self.body.x += self.body.vx * dt
        self._resolve_x(platforms)

        self.body.y += self.body.vy * dt
        self._resolve_y(platforms)

    def draw(self, screen, camera):
        rect = pygame.Rect(self.body.x, self.body.y, self.WIDTH, self.HEIGHT)
        sr = camera.apply(rect)
        pygame.draw.rect(screen, (220, 70, 70), sr)
        pygame.draw.rect(screen, (255, 210, 210), sr, 2)
        eye_offset = sr.width // 4 if self.body.vx >= 0 else -sr.width // 4
        eye_pos = (sr.centerx + eye_offset, sr.y + sr.height // 4)
        pygame.draw.circle(screen, (255, 255, 0), eye_pos, max(2, sr.width // 7))


# --- FlyingEnemy ---

class FlyingEnemy(EnemyBase):
    WIDTH = 28
    HEIGHT = 28
    HOVER_AMP = 80
    CHASE_SPEED = 200

    def __init__(self, x, y, detection_range=400):
        super().__init__(x, y, detection_range)
        self.body.use_gravity = False
        self.hover_timer = 0.0
        self.flying = True
        self.state_machine = EnemyStateMachine(HoverState())

    def update(self, dt, player, platforms):
        self.hover_timer += dt
        self.state_machine.update(self, player, platforms, dt)

        self.body.x += self.body.vx * dt
        self.body.y += self.body.vy * dt

    def draw(self, screen, camera):
        rect = pygame.Rect(self.body.x, self.body.y, self.WIDTH, self.HEIGHT)
        sr = camera.apply(rect)
        pygame.draw.rect(screen, (160, 80, 240), sr)
        pygame.draw.rect(screen, (220, 180, 255), sr, 2)
        pygame.draw.circle(screen, (255, 255, 100), sr.center, max(3, sr.width // 5))
