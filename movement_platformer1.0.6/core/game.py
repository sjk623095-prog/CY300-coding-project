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
        # --- Transition in progress: freeze physics, advance the fade ---
        if self.level_manager.is_transitioning():
            result = self.level_manager.update_transition(self.player, dt)
            if result == 'switched':
                # Room has changed at peak black — snap camera so it doesn't lerp from old room
                self.camera.offset_x = self.player.body.x - (SCREEN_WIDTH / 2) / self.camera.zoom
                self.camera.offset_y = self.player.body.y - (SCREEN_HEIGHT / 2) / self.camera.zoom
                self.last_safe_pos = (self.player.body.x, self.player.body.y)
            self.room = self.level_manager.current_room
            self.room.update(dt, self.player, self.room.platforms)
            return

        # --- Normal gameplay ---
        self.player.update(dt)

        self.physics.step(dt)

        # --- X movement ---
        self.player.body.x += self.player.body.vx * dt
        resolve_collisions_x(self.player, self.room.platforms)

        # --- Y movement ---
        self.player.body.y += self.player.body.vy * dt

        # CHECK TRANSITION BEFORE Y COLLISION — starts fade, freezes player
        if self.level_manager.check_transitions(self.player):
            self.room = self.level_manager.current_room
            return

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

        # Check if player stepped on a skill unlock tile
        self.level_manager.check_skill_unlocks(self.player)

        # Hazard damage (spikes, pits)
        if self.level_manager.check_hazards(self.player, self.last_safe_pos):
            if self.player.take_damage():
                self.lives -= 1
                print("Lives:", self.lives)
                if self.lives <= 0:
                    self.reset_game()

        # Always keep current room updated
        self.room = self.level_manager.current_room

        self.room.update(dt, self.player, self.room.platforms)

        # Enemy contact damage
        player_rect = pygame.Rect(int(self.player.body.x), int(self.player.body.y), 20, 40)
        for enemy in self.room.enemies:
            enemy_rect = pygame.Rect(int(enemy.body.x), int(enemy.body.y), enemy.WIDTH, enemy.HEIGHT)
            if player_rect.colliderect(enemy_rect):
                if self.player.take_damage():
                    self.lives -= 1
                    print("Lives:", self.lives)
                    if self.lives <= 0:
                        self.reset_game()
                break

    def draw(self):
        self.screen.fill((30, 30, 40))

        self.room.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)

        self.draw_hud()

        # Fade-to-black overlay for room transitions
        alpha = int(self.level_manager.transition_alpha)
        if alpha > 0:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(alpha)
            self.screen.blit(overlay, (0, 0))

        pygame.display.flip()

    def draw_hud(self):
        font = pygame.font.SysFont(None, 28)
        small_font = pygame.font.SysFont(None, 22)
        pad = 10

        # --- Lives as pips ---
        label_surf = font.render("Lives:", True, (255, 255, 255))
        self.screen.blit(label_surf, (pad, pad))

        pip_size = 14
        pip_gap = 4
        pip_x = pad + label_surf.get_width() + 8
        for i in range(5):
            color = (220, 50, 50) if i < self.lives else (80, 80, 80)
            pygame.draw.rect(self.screen, color,
                             (pip_x + i * (pip_size + pip_gap), pad + 2, pip_size, pip_size))

        # --- Skill indicators ---
        skills = [
            ("DASH",     self.player.has_dash),
            ("LEVITATE", self.player.has_levitate),
        ]
        skill_y = pad + label_surf.get_height() + 8
        for name, unlocked in skills:
            color = (80, 220, 120) if unlocked else (90, 90, 90)
            label = small_font.render(name, True, color)
            self.screen.blit(label, (pad, skill_y))
            skill_y += label.get_height() + 4

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

        self.player.body.vx = 0
        self.player.body.vy = 0
        self.player.invincibility_timer = 0.0

        # Reset safe position
        self.last_safe_pos = (self.player.body.x, self.player.body.y)
