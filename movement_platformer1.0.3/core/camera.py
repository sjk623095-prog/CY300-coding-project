import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0

    def follow(self, target, dt):
        # Center camera on target
        target_x = target.body.x - (SCREEN_WIDTH / 2) / self.zoom
        self.offset_x += (target_x - self.offset_x) * 10 * dt

        target_y = target.body.y - (SCREEN_HEIGHT / 2) / self.zoom
        self.offset_y += (target_y - self.offset_y) * 10 * dt 
        
    def apply(self, rect):
        return pygame.Rect(
        int((rect.x - self.offset_x) * self.zoom),
        int((rect.y - self.offset_y) * self.zoom),
        int(rect.width * self.zoom),
        int(rect.height * self.zoom)
    )

    def apply_pos(self, x, y):
        return int((x - self.offset_x) * self.zoom), int((y - self.offset_y) * self.zoom)
        