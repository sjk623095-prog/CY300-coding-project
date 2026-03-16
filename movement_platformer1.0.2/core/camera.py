class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0

    def follow(self, player):
        self.offset_x = player.body.x - 640
        