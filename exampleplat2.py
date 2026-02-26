import pygame
import sys

pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.6
PLAYER_SPEED = 5
JUMP_STRENGTH = -12
MAX_JUMPS = 2

# --- Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer - Multiple Levels")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


# ==============================
# Level Data
# ==============================
levels = [
    {
        "player_start": (100, 400),
        "platforms": [
            (0, 550, 800, 50),
            (300, 450, 200, 20),
        ],
        "obstacles": [
            (400, 530, 50, 20),
        ],
        "goal": (700, 500, 50, 50),
    },
    {
        "player_start": (50, 400),
        "platforms": [
            (0, 550, 800, 50),
            (150, 450, 150, 20),
            (400, 380, 150, 20),
            (650, 300, 120, 20),
        ],
        "obstacles": [
            (300, 530, 100, 20),
            (550, 530, 100, 20),
        ],
        "goal": (700, 250, 50, 50),
    },
]


# ==============================
# Player Class
# ==============================
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.vel_x = 0
        self.vel_y = 0
        self.jumps = 0

    def handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_LEFT]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vel_x = PLAYER_SPEED

        if keys[pygame.K_SPACE] and self.jumps < MAX_JUMPS:
            self.vel_y = JUMP_STRENGTH
            self.jumps += 1

    def apply_gravity(self):
        self.vel_y += GRAVITY

    def move(self, platforms):
        # Horizontal movement
        self.rect.x += self.vel_x
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_x > 0:
                    self.rect.right = platform.left
                if self.vel_x < 0:
                    self.rect.left = platform.right

        # Vertical movement
        self.rect.y += self.vel_y
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.jumps = 0
                if self.vel_y < 0:
                    self.rect.top = platform.bottom
                    self.vel_y = 0

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 200, 255), self.rect)


# ==============================
# Level Loader
# ==============================
def load_level(index):
    data = levels[index]
    platforms = [pygame.Rect(*p) for p in data["platforms"]]
    obstacles = [pygame.Rect(*o) for o in data["obstacles"]]
    goal = pygame.Rect(*data["goal"])
    player = Player(*data["player_start"])
    return player, platforms, obstacles, goal


# ==============================
# Game Setup
# ==============================
current_level = 0
player, platforms, obstacles, goal = load_level(current_level)


# ==============================
# Game Loop
# ==============================
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # --- Update ---
    player.handle_input(keys)
    player.apply_gravity()
    player.move(platforms)

    # --- Obstacle Collision (Reset Level) ---
    for obstacle in obstacles:
        if player.rect.colliderect(obstacle):
            player, platforms, obstacles, goal = load_level(current_level)

    # --- Fall Off Map Reset ---
    if player.rect.top > HEIGHT:
        player, platforms, obstacles, goal = load_level(current_level)

    # --- Goal Collision (Next Level) ---
    if player.rect.colliderect(goal):
        current_level += 1
        if current_level >= len(levels):
            current_level = 0
        player, platforms, obstacles, goal = load_level(current_level)

    # --- Draw ---
    screen.fill((30, 30, 40))

    # Platforms
    for platform in platforms:
        pygame.draw.rect(screen, (100, 255, 100), platform)

    # Obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, (255, 60, 60), obstacle)

    # Goal
    pygame.draw.rect(screen, (255, 215, 0), goal)

    player.draw(screen)

    # Level Text
    level_text = font.render(f"Level {current_level + 1}", True, (255, 255, 255))
    screen.blit(level_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
