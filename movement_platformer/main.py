import pygame
import sys

from settings import *
# hello from Cooper
def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Scifi Space Platformer") #Name of game here

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000  # delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 40))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()