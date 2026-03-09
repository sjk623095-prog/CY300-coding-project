class Room:
    def __init__(self):
        self.platforms = []
        self.enemies = []
        self.hazards = []

    def update(self, dt):
        pass

    def draw(self, screen):
        for p in self.platforms:
            pygame.draw.rect(screen, (100,100,100), p)