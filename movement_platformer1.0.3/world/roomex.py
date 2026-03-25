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

#Updated
    def __init__(self, tile_map, tile_size=40, exits=None):
        self.platforms = []
        self.hazards = [] # NEW: List for spikes/lava
        self.tile_size = tile_size
        self.exits = exits if exits else []
        
        # Calculate room dimensions for the camera
        self.width = len(tile_map[0]) * tile_size
        self.height = len(tile_map) * tile_size

        for row_index, row in enumerate(tile_map):
            for col_index, char in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                
                if char == "X":
                    self.platforms.append(pygame.Rect(x, y, self.tile_size, self.tile_size))
                elif char == "S": # NEW: 'S' for Spikes
                    # Make the hazard slightly smaller than a full block for fair gameplay
                    self.hazards.append(pygame.Rect(x + 5, y + 20, self.tile_size - 10, self.tile_size - 20))


    def update(self, dt):
        pass

    # def draw(self, screen, camera):
    #     for p in self.platforms:
    #         screen_rect = camera.apply(p)
    #         pygame.draw.rect(screen, (100,100,100), screen_rect)

#Updated
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