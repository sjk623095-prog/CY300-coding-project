import pygame
from world.roomex import Room

class LevelManager:
    def __init__(self):
        self.rooms = {
            "start_hub": Room(
                tile_map=[
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "X                            X",
                    "X      XXXXX                 X",
                    "X                            X",
                    "XXXXXXXXXXXXXXXX      XXXXXXXX",
                ],
                exits=[(pygame.Rect(640, 440, 100, 100), "pit_room", (100, 100))]
            ),

            "pit_room": Room(
                tile_map=[
                    "XXXX      XXXXXXXXXXXXXXXXXXXX",
                    "X                            X",
                    "X     XXXX                   X",
                    "X            XXXX            X",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                ],
                exits=[
                    # This exit now leads to our new Level 3!
                    (pygame.Rect(1150, 0, 50, 400), "vertical_climb", (100, 300))
                ]
            ),

            # --- ADD LEVEL 3 HERE ---
            "vertical_climb": Room(
                tile_map=[
                    "XXXXXXXXXX      XXXXXXXXXX",
                    "X                        X",
                    "X   XXXX                 X",
                    "X            XXXX        X",
                    "X   XXXX                 X",
                    "X            XXXX        X",
                    "X                        X",
                    "XXXXXXXXXX      XXXXXXXXXX",
                ],
                exits=[
                    # Exit at the top takes you back to the very start
                    (pygame.Rect(400, 0, 100, 40), "start_hub", (200, 200))
                ]
            )
        }
        self.current_room_key = "start_hub"
        self.current_room = self.rooms[self.current_room_key]

    def check_transitions(self, player):
        player_rect = pygame.Rect(player.body.x, player.body.y, 20, 40)
        
        for rect, target_room, spawn_pos in self.current_room.exits:
            if player_rect.colliderect(rect):
                self.current_room_key = target_room
                self.current_room = self.rooms[target_room]
                
                # Teleport player and reset velocity
                player.body.x, player.body.y = spawn_pos
                player.body.vx = 0
                player.body.vy = 0
                return True
        return False
    
    def check_hazards(self, player):
        player_rect = pygame.Rect(player.body.x, player.body.y, 20, 40)
        
        for hazard in self.current_room.hazards:
            if player_rect.colliderect(hazard):
                # Reset player to a safe spot (you can customize this per room)
                player.body.x, player.body.y = 100, 100 
                player.body.vx, player.body.vy = 0, 0
                return True
        return False