import pygame
from settings import *
from core.player import Player
from core.camera import Camera
from world.roomex import Room
from physics.physics_engine import physics_engine_1
from physics.collision_handler import resolve_collisions_x
from physics.collision_handler import resolve_collisions_y
from world.level_manager import LevelManager
class Game:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Scifi Space Platformer")

        self.clock = pygame.time.Clock()
        self.running = True

        self.camera = Camera()

        self.physics = physics_engine_1()

        # create objects
        self.player = Player(200, 200)
        self.physics.add_body(self.player.body)
        self.room = Room() 

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        self.player.update(dt)

        self.physics.step(dt)

        # --- X movement ---
        self.player.body.x += self.player.body.vx * dt
        resolve_collisions_x(self.player, self.room.platforms)

        # --- Y movement ---
        self.player.body.y += self.player.body.vy * dt
        resolve_collisions_y(self.player, self.room.platforms)

        
        #DYNAMIC ZOOMING

        target_zoom = 1.3

        if self.player.body.vy > 500:   # falling fast
            target_zoom = 1.0

        self.camera.zoom += (target_zoom - self.camera.zoom) * 5 * dt

        self.camera.follow(self.player, dt)

        self.room.update(dt)

    def draw(self):
        self.screen.fill((30,30,40))

        self.room.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)

        pygame.display.flip()


