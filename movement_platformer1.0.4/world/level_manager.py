import pygame
from world.roomex import Room


class LevelManager:
    def __init__(self):
        self.transition_cooldown = 0
        self.rooms = {
            "start_hub": Room(
                tile_map=[
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "X                                                      X",
                    "X                                                      X",
                    "X                                                      X",
                    "X                                                      X",
                    "X                                                      X",
                    "X      XXXXXXXXX                                       X",
                    "X                             XXXXXXX                  X",
                    "X                  XXXXXX                              X",
                    "X                                                      E",
                    "X                                   SSS                E",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                ],
            ),

            "pit_room": Room(
                tile_map=[
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "    E                                                     X",
                    "    E                                                     X",
                    "XXXXXXXXXXXXXXXXXXX                                       X",
                    "X                 X               XXXXXXX                 X",
                    "X                 X                                       X",
                    "X                 X     S                                 X",
                    "X                     XXXXXX                              X",
                    "X                                                         X",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX       XXXXXXXXXXXXXXXXXXXXXXX",
                    "X                           X       X                  X",
                    "X                           X       X                  X",
                    "X                           X       X                  X",
                    "X                           X       X                  X",
                    "X                           X       X                  X",
                    "X                           X       X                  X",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXEEEEEEEXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXEEEEEEEXXXXXXXXXXXXXXXXXXXX",
                    "X                           X       X                  X",
                    "X                           X       X                  X",
                    "X                           X       X                  X",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                ],
            ),

            # --- ADD LEVEL 3 HERE ---
            "vertical_climb": Room(
                tile_map=[
                    "XXXXXXEEEEEEEXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXEEEEEEEXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXX       X                                         X",
                    "XXXXXX       X                                         X",
                    "XXXXXX       X                                         X",
                    "X                                                      X",
                    "X        XX                                            X",
                    "X                                                      X",
                    "X                                                      X",
                    "X                                                      X",
                    "X    XXXXXX                                            X",
                    "X                 XXXXXXX                              X",
                    "X                                                      X",
                    "X                                  XXXXXXX             X",
                    "X                                                      X",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                ],
            )
        }
        self.current_room_key = "start_hub"
        self.current_room = self.rooms[self.current_room_key]
        # --- Link exits ---
        self.link_bidirectional("start_hub", 0, "pit_room", 0, "down", "up")
        self.link_bidirectional("pit_room", 1, "vertical_climb", 0, "right", "left")

    def link_exit(self, room_name, exit_index, target, target_exit_index, direction):
        # this system sets up linking rooms by the exits and not pre-determined start points
        rect = self.rooms[room_name].exits[exit_index][0]
        self.rooms[room_name].exits[exit_index] = (
            rect,
            target,
            None,              # spawn no longer used
            direction,
            target_exit_index  # NEW
        )

    def link_bidirectional(self, room_a, exit_a, room_b, exit_b, dir_a, dir_b):
        self.link_exit(room_a, exit_a, room_b, exit_b, dir_a)
        self.link_exit(room_b, exit_b, room_a, exit_a, dir_b)

    def check_hazards(self, player, safe_pos): #checks for hazards and employs a reset if the player hits them
        player_rect = pygame.Rect(player.body.x, player.body.y, 20, 40)

        for hazard in self.current_room.hazards:
            if player_rect.colliderect(hazard):

                # --- Reset to room spawn ---
                x, y = safe_pos

                player_rect = pygame.Rect(x, y, 20, 40)

                safe = False
                attempts = 0

                while not safe and attempts < 5:
                    safe = True

                    for hazard in self.current_room.hazards:
                        if player_rect.colliderect(hazard):
                            safe = False
                            break

                    if not safe:
                        y -= 40
                        player_rect.y = y

                    attempts += 1


                player.body.x = x
                player.body.y = y

                # --- Reset velocity ---
                player.body.vx = 0
                player.body.vy = 0

                return True

        return False

    def check_transitions(self, player):
        if self.transition_cooldown > 0:
            self.transition_cooldown -= 1
            return False
        player_rect = pygame.Rect(player.body.x, player.body.y, 20, 40)

        for rect, target_room, spawn_pos, direction, target_exit_index in self.current_room.exits:
            if player_rect.colliderect(rect):
                # Horizontal checks
                if direction == "right" and player.body.vx < 0:
                    continue
                if direction == "left" and player.body.vx > 0:
                    continue

                # Vertical checks
                if direction == "down" and player.body.vy < 0:
                    continue
                if direction == "up" and player.body.vy > 0:
                    continue
                self.current_room_key = target_room
                self.current_room = self.rooms[target_room]

                # Spawn in room
                # Get target exit index
                target_exit = target_exit_index

                # Get the exit rect in the NEW room
                exit_rect = self.current_room.exits[target_exit][0]

                # Spawn at that exit
                x = exit_rect.centerx - 10   # half player width
                y = exit_rect.centery - 20   # half player height

                # small offset instead of overwrite
                offset = 40

                padding = 5

                if direction == "right":
                    x = exit_rect.right + padding

                elif direction == "left":
                    x = exit_rect.left - 20 - padding  # player width = 20

                elif direction == "down":
                    y = exit_rect.bottom + padding

                elif direction == "up":
                    y = exit_rect.top - 40 - padding   # player height = 40

                player.body.x = x
                player.body.y = y

                # Reset velocity
                player.body.vx = 0
                player.body.vy = 0

                self.transition_cooldown = 80  # ~0.25 sec

                return True

        return False
