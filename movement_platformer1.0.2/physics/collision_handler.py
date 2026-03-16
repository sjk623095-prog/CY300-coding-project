import pygame
#from player import Player

def resolve_platform_collisions(player, platforms):
    player_rect = pygame.Rect(int(player.body.x), int(player.body.y), 20, 40)
    player.on_ground = False
    for p in platforms:
        if player_rect.colliderect(p):
            
            #falling onto platform
            if player.body.vy > 0:
                player.body.y = p.top -40
                player.body.vy = 0
                player.on_ground = True
