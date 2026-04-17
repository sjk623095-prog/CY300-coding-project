import pygame
from world.roomex import Room

FADE_SPEED = 500  # alpha units per second — 255 / 500 ≈ 0.51s to full black


class LevelManager:
    def __init__(self):
        self.transition_cooldown = 0
        self.transition_state = 'idle'   # 'idle', 'fade_out', 'fade_in'
        self.transition_alpha = 0.0
        self._pending = None             # (target_room_key, x, y)
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
                    "X                                                   N  E",
                    "X                                   SSS                E",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                ],
            ),

            "pit_room": Room(
                tile_map=[
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "    E N                                                   X",
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
                    "X                           XN      X                  X",
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
                    "XXXXXX  N    X                                         X",
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

    def is_transitioning(self):
        return self.transition_state != 'idle'

    def update_transition(self, player, dt):
        """Advance the fade. Returns 'switched' when room swaps (caller snaps camera), 'done' when finished."""
        if self.transition_state == 'idle':
            return None

        if self.transition_state == 'fade_out':
            self.transition_alpha += FADE_SPEED * dt
            if self.transition_alpha >= 255:
                self.transition_alpha = 255.0
                target_room, x, y = self._pending
                self.current_room_key = target_room
                self.current_room = self.rooms[target_room]
                player.body.x = x
                player.body.y = y
                player.body.vx = 0
                player.body.vy = 0
                self._pending = None
                self.transition_state = 'fade_in'
                return 'switched'

        elif self.transition_state == 'fade_in':
            self.transition_alpha -= FADE_SPEED * dt
            if self.transition_alpha <= 0:
                self.transition_alpha = 0.0
                self.transition_state = 'idle'
                self.transition_cooldown = 10
                return 'done'

        return None

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
        if self.transition_state != 'idle':
            return False
        if self.transition_cooldown > 0:
            self.transition_cooldown -= 1
            return False

        player_rect = pygame.Rect(player.body.x, player.body.y, 20, 40)

        for rect, target_room, spawn_pos, direction, target_exit_index in self.current_room.exits:
            if player_rect.colliderect(rect):
                if direction == "right" and player.body.vx < 0:
                    continue
                if direction == "left" and player.body.vx > 0:
                    continue
                if direction == "down" and player.body.vy < 0:
                    continue
                if direction == "up" and player.body.vy > 0:
                    continue

                # Use the N-tile start point defined in the target room
                start = self.rooms[target_room].start_points[target_exit_index]
                x, y = start

                # Freeze player and start fade-to-black
                player.body.vx = 0
                player.body.vy = 0
                self._pending = (target_room, x, y)
                self.transition_state = 'fade_out'
                self.transition_alpha = 0.0

                return True

        return False
