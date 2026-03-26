import pygame
from settings import *
from core.player import Player
from core.camera import Camera
#from world.roomex import Room
from physics.physics_engine import physics_engine_1
from physics.collision_handler import resolve_collisions_x
from physics.collision_handler import resolve_collisions_y
from world.level_manager import LevelManager


class Game:

    def __init__(self):
        # init pygame
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Scifi Space Platformer")

        # init level manager
        self.level_manager = LevelManager()
        self.room = self.level_manager.current_room

        # init time (for physics calcs)
        self.clock = pygame.time.Clock()
        self.running = True

        # init camera
        self.camera = Camera()

        # init physics
        self.physics = physics_engine_1()

        # create objects
        self.player = Player(200, 200)
        self.physics.add_body(self.player.body)

        #last safe position tracker
        self.last_safe_pos = (self.player.body.x, self.player.body.y)

        self.lives = 5

    def run(self):
        # setting up a while loop for FPS/updating and running the game
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

        # CHECK TRANSITION BEFORE COLLISION
        if self.level_manager.check_transitions(self.player):
            self.last_safe_pos = (self.player.body.x, self.player.body.y)

        resolve_collisions_y(self.player, self.room.platforms)

        # Update safe position ONLY when on ground
        if self.player.on_ground:
            self.last_safe_pos = (self.player.body.x, self.player.body.y)

        # DYNAMIC ZOOMING

        target_zoom = 1.3

        if self.player.body.vy > 500:   # falling fast
            target_zoom = 1.0

        self.camera.zoom += (target_zoom - self.camera.zoom) * 5 * dt

        self.camera.follow(self.player, dt)

        # room updates for transitions and hazards
        if self.level_manager.check_hazards(self.player, self.last_safe_pos):
            self.lives -= 1
            print("Lives:", self.lives)

            if self.lives <= 0:
                self.reset_game()


        # Always keep current room updated
        self.room = self.level_manager.current_room

        self.room.update(dt)

    def draw(self):
        self.screen.fill((30, 30, 40))

        self.room.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)

        pygame.display.flip()

    def reset_game(self):
        print("Game Over - Resetting")

        # Reset lives
        self.lives = 5

        # Reset level
        self.level_manager = LevelManager()
        self.room = self.level_manager.current_room

        # Reset player position
        spawn = self.room.spawn_point if self.room.spawn_point else (200, 200)
        self.player.body.x, self.player.body.y = spawn

        # Reset velocity
        self.player.body.vx = 0
        self.player.body.vy = 0

        # Reset safe position
        self.last_safe_pos = (self.player.body.x, self.player.body.y)
