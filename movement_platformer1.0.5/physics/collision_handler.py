import pygame
#from player import Player

def resolve_collisions_x(player, platforms):

    player.on_wall = False
    player_rect = pygame.Rect(player.body.x, player.body.y, 20, 40)

    for p in platforms:
        if player_rect.colliderect(p):

            if player.body.vx > 0:  # moving right
                player.body.x = p.left - 20
                player.body.vx = 0

                player.on_wall = True
                player.wall_dir = "right"

            elif player.body.vx < 0:  # moving left
                player.body.x = p.right
                player.body.vx = 0

                player.on_wall = True
                player.wall_dir = "left"

            player.body.vx = 0

            # update rect after correction
            player_rect.x = player.body.x

def resolve_collisions_y(player, platforms):
    player_rect = pygame.Rect(player.body.x, player.body.y, 20, 40)

    player.on_ground = False

    for p in platforms:
        if player_rect.colliderect(p):

            if player.body.vy > 0:  # falling
                player.body.y = p.top - 40
                player.body.vy = 0
                player.on_ground = True

            elif player.body.vy < 0:  # hitting ceiling
                player.body.y = p.bottom
                player.body.vy = 0

            player_rect.y = player.body.y

"""def resolve_platform_collisions(player, platforms):
    player_rect = pygame.Rect(player.body.x, player.body.y, 20, 40)
    player.on_ground = False
    for p in platforms:
        if player_rect.colliderect(p):
            
            #falling onto platform
            if player.body.vy > 0:
                player.body.y = p.top -40
                player.body.vy = 0
                player.on_ground = True"""

            #hitting platform side