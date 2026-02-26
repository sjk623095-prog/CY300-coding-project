import pygame
import sys

pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
PLAYER_SPEED = 5
JUMP_STRENGTH = -12

# --- Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Platformer - pygame-ce")
clock = pygame.time.Clock()

# --- Player ---
player = pygame.Rect(100, 400, 50, 50)
player_vel_y = 0
on_ground = False

# --- Platforms ---
platforms = [
    pygame.Rect(0, 550, 800, 50),
    pygame.Rect(200, 450, 200, 20),
    pygame.Rect(500, 350, 200, 20),
]

# --- Game Loop ---
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Input ---
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED
    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = JUMP_STRENGTH
        on_ground = False

    # --- Gravity ---
    player_vel_y += GRAVITY
    player.y += player_vel_y

    # --- Collision ---
    on_ground = False
    for platform in platforms:
        if player.colliderect(platform) and player_vel_y > 0:
            player.bottom = platform.top
            player_vel_y = 0
            on_ground = True

    # --- Drawing ---
    screen.fill((30, 30, 40))

    pygame.draw.rect(screen, (0, 200, 255), player)
    for platform in platforms:
        pygame.draw.rect(screen, (100, 255, 100), platform)

    pygame.display.flip()

pygame.quit()
sys.exit()
