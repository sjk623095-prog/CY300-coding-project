import pygame
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Scifi Space Platformer")

        self.clock = pygame.time.Clock()
        self.running = True

        self.current_room = None
        self.player = None
        self.camera = None

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        if self.current_room:
            self.current_room.update(dt)

    def render(self):
        self.screen.fill((30,30,40))
        if self.current_room:
            self.current_room.draw(self.screen)

        pygame.display.flip()