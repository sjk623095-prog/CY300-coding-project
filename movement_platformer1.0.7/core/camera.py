import pygame


class Camera:
    """Tracks and smoothly follows the player, converting world coords to screen coords with zoom."""

    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0

    def follow(self, target, dt, screen_w, screen_h):
        """Smoothly lerp camera to keep target centered on screen. Requires current screen dimensions."""
        target_x = target.body.x - (screen_w / 2) / self.zoom
        self.offset_x += (target_x - self.offset_x) * 10 * dt

        target_y = target.body.y - (screen_h / 2) / self.zoom
        self.offset_y += (target_y - self.offset_y) * 10 * dt

    def apply(self, rect):
        """Return a screen-space pygame.Rect for a world-space rect."""
        return pygame.Rect(
            int((rect.x - self.offset_x) * self.zoom),
            int((rect.y - self.offset_y) * self.zoom),
            int(rect.width * self.zoom),
            int(rect.height * self.zoom)
        )

    def apply_pos(self, x, y):
        """Return screen-space (x, y) for world-space coordinates."""
        return int((x - self.offset_x) * self.zoom), int((y - self.offset_y) * self.zoom)
        