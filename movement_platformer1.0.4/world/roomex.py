import pygame


class Room:
    # def __init__(self):
    #     self.platforms = [
    #         pygame.Rect(0,680,2000,40), #ground
    #         pygame.Rect(400,600,200,20),
    #         pygame.Rect(200,450,200,20),
    #         pygame.Rect(700,450,200,20),
    #         pygame.Rect(1100,350,200,20),
    #         pygame.Rect(0,500,20,500)
    #     ]
    #     self.enemies = []
    #     self.hazards = []

    def __init__(self, tile_map, tile_size=64):
        self.platforms = []
        self.hazards = []  # NEW: List for spikes/lava
        exit_tiles = [] #exit setting
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
                    
                elif char == "S":  # NEW: 'S' for Spikes
                    # Make the hazard slightly smaller than a full block for fair gameplay
                    self.hazards.append(pygame.Rect(
                        x + 5, y + 20, self.tile_size - 10, self.tile_size - 20))
                
                elif char == "P":
                    self.spawn_point = (x, y)

                elif char == "E":
                    exit_tiles.append((x, y))
        self.exits = self.build_exit_zones(exit_tiles)

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

    def update(self, dt):
        pass

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
