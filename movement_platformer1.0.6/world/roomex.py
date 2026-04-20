import pygame
import math
from enemies.enemies import PatrolEnemy, FlyingEnemy


class Room:
    def __init__(self, tile_map, tile_size=64):
        self.platforms = []
        self.hazards = []
        self.unlock_tiles = []   # list of [rect, skill_name] — mutable for removal
        self.enemies = []
        exit_tiles = []
        n_tiles = []          # entrance spawn markers — one per exit zone
        self.spawn_point = None
        self.tile_size = tile_size

        # Calculate room dimensions for the camera
        self.width = len(tile_map[0]) * tile_size
        self.height = len(tile_map) * tile_size

        for row_index, row in enumerate(tile_map):
            for col_index, char in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size

                if char == "X":
                    self.platforms.append(pygame.Rect(
                        x, y, self.tile_size, self.tile_size))

                elif char == "S":
                    self.hazards.append(pygame.Rect(
                        x + 5, y + 20, self.tile_size - 10, self.tile_size - 20))

                elif char == "P":
                    self.enemies.append(PatrolEnemy(x, y))

                elif char == "F":
                    self.enemies.append(FlyingEnemy(x, y))

                elif char == "E":
                    exit_tiles.append((x, y))

                elif char == "N":
                    n_tiles.append((x, y))

                elif char == "D":
                    self.unlock_tiles.append(
                        [pygame.Rect(x, y, self.tile_size, self.tile_size), "dash"])

                elif char == "L":
                    self.unlock_tiles.append(
                        [pygame.Rect(x, y, self.tile_size, self.tile_size), "levitate"])

        self.exits = self.build_exit_zones(exit_tiles)
        self.start_points = self._match_start_points(n_tiles)

    #This method sets up

    def build_exit_zones(self, tiles):
        visited = set()
        zones = []

        for tile in tiles:
            if tile in visited:
                continue

            # flood fill to group connected tiles
            stack = [tile]
            group = []

            while stack:
                t = stack.pop()
                if t in visited:
                    continue

                visited.add(t)
                group.append(t)

                x, y = t

                neighbors = [
                    (x + self.tile_size, y),
                    (x - self.tile_size, y),
                    (x, y + self.tile_size),
                    (x, y - self.tile_size),
                ]

                for n in neighbors:
                    if n in tiles and n not in visited:
                        stack.append(n)

            # build one big rect from group
            xs = [t[0] for t in group]
            ys = [t[1] for t in group]

            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)

            width = (max_x - min_x) + self.tile_size
            height = (max_y - min_y) + self.tile_size

            rect = pygame.Rect(min_x, min_y, width, height)

            zones.append((rect, None, None, None, None))

        return zones

    def _match_start_points(self, n_tiles):
        """For each exit zone pick the nearest N tile as the spawn point. Returns list indexed by exit."""
        result = []
        for rect, *_ in self.exits:
            ex, ey = rect.centerx, rect.centery
            best = None
            best_dist = float('inf')
            for nx, ny in n_tiles:
                d = math.dist((ex, ey), (nx + self.tile_size // 2, ny + self.tile_size // 2))
                if d < best_dist:
                    best_dist = d
                    best = (nx, ny)
            result.append(best)
        return result

    def update(self, dt, player=None, platforms=None):
        if player is not None and platforms is not None:
            for enemy in list(self.enemies):
                enemy.update(dt, player, platforms)
                if enemy.touches_hazard(self.hazards):
                    self.enemies.remove(enemy)

    # def draw(self, screen, camera):
    #     for p in self.platforms:
    #         screen_rect = camera.apply(p)
    #         pygame.draw.rect(screen, (100,100,100), screen_rect)

    # updated draw
    def draw(self, screen, camera):
        # Draw Platforms
        for p in self.platforms:
            screen_rect = camera.apply(p)
            pygame.draw.rect(screen, (70, 70, 90), screen_rect)
            pygame.draw.rect(screen, (100, 100, 120), screen_rect, 1)

        # NEW: Draw Hazards (Red triangles or rectangles)
        for h in self.hazards:
            screen_rect = camera.apply(h)
            pygame.draw.rect(screen, (255, 50, 50), screen_rect)

        for rect, _, _, _, _ in self.exits:
            screen_rect = camera.apply(rect)
            pygame.draw.rect(screen, (0, 255, 0), screen_rect, 2)

        # Draw unlock tiles: orange = dash, cyan = levitate
        for tile in self.unlock_tiles:
            rect, skill = tile
            screen_rect = camera.apply(rect)
            color = (255, 165, 0) if skill == "dash" else (0, 220, 255)
            pygame.draw.rect(screen, color, screen_rect)
            pygame.draw.rect(screen, (255, 255, 255), screen_rect, 2)

        for enemy in self.enemies:
            enemy.draw(screen, camera)
