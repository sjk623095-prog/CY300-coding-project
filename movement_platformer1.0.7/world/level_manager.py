import pygame
from world.roomex import Room

FADE_SPEED = 500  # alpha units per second — 255 / 500 ≈ 0.51s to full black


class LevelManager:
    """Owns all rooms, links their exits bidirectionally, and manages fade-transition and hazard/skill-unlock logic."""

    def __init__(self):
        self.transition_cooldown = 0
        self.transition_state = 'idle'   # 'idle', 'fade_out', 'fade_in'
        self.transition_alpha = 0.0
        self._pending = None             # (target_room_key, x, y)
        self.rooms = {
            "start_hub": Room(
                tile_map=[
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "E                                                      X",
                    "E X                                                    X",
                    "XXX                                                    X",
                    "X                                                      X",
                    "X                                                      X",
                    "X                                                      X",
                    "X                                                      X",
                    "X                                                      X",
                    "X                                     F                X",
                    "X                                                      X",
                    "X                                                      X",
                    "X          N                                           X",
                    "X                             XXXXXXX                  X",
                    "X                     XXX                              X",
                    "XXXXXXX   XXXXX                                     N  E",
                    "X                        P          SSS                E",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                ],
            ),

            "pit_room": Room(
                tile_map=[
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "    E N                                                   X",
                    "    E                                                     X",
                    "XXXXXXXXXXXXXXXXXXX                           FF          X",
                    "X                 X               XXXXXXX                 X",
                    "X                 X                                       X",
                    "X                 X     S                                 X",
                    "X                     XXXXXX                              X",
                    "X     P                                                   X",
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
                    "X                                        F             X",
                    "X        XX                                            X",
                    "X                                                      X",
                    "X                                                      X",
                    "X                                                      X",
                    "X    XXXXXX         P                                  X",
                    "X                 XXXXXXX                              X",
                    "X                                                      X",
                    "X                                  XXXXXXX           N E",
                    "X          P                                           E",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                ],
            ),
            "parkour": Room(
                tile_map=[
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "E            X           F        X                          X                                    E",
                    "E N          X                    X         F           X    X            XX                    N E",
                    "XXXXX        X                    X                     X    X                                 XXXX",
                    "X            X          XXX       X                     X    X         XX       F                 X",
                    "X            X                    X                     X    X                         XX         X",
                    "X                X                      XXX             X    XXXXX                                X",
                    "XXXX             X                              XXXXX   X                        XX               X",
                    "X       XX       X                X                     X          XX                             X",
                    "XSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSXSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                ],
            ),

            # --- Room 5: spike-pit traverse — hop across floating platforms above a spike floor ---
            "spike_traverse": Room(
                tile_map=[
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "X                                                                                        X",
                    "X                                                               F                        X",
                    "E                                        F                                               E",
                    "E                                                                                        E",
                    "EN                    XXXXX           XXXXX            XXXXX            XXXXX        N   E",
                    "XXXX                                                                              XXXXXXXX",
                    "X          XXXXX            XXXXX           XXXXX            XXXXX                       X",
                    "X                                                                                        X",
                    "X                                                                                        X",
                    "XSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSX",
                    "XSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                ],
            ),

            # --- Room 7: dash canyon — wide spike-filled canyon, D unlock on first platform ---
            # Gaps are 13-14 tiles wide (832-896 px). Normal max single jump covers ~12.5 tiles
            # (800 px/s * 1.0 s air time). Dash (1400 px/s burst) makes crossing reliable.
            # Exit 0 = left side (entry from vertical_gauntlet)
            # Exit 1 = right side (leads to levitate_ascent)
            "dash_canyon": Room(
                tile_map=[
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "X                                 F                                                         X",
                    "X                                                                                           X",
                    "EN             D                                  XXXXXXX           F                       E",
                    "E            XXXXXXXXXX XXXXXXXXXXXX                                                      N E",
                    "XXXXXXXXX                                                                           XXXXXXXXXX",
                    "X                          XXXXXXXXXX                           XXXXXXXXXX                  X",
                    "X                                                                                           X",
                    "X                                                                                           X",
                    "X                                                                                           X",
                    "XSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                ],
            ),

            # --- Room 8: levitate ascent — tall vertical shaft, L unlock on low platform ---
            # Vertical gaps between platforms are 8 rows = 512 px.
            # Max double-jump height = 450 px < 512 px, so these gaps require levitate (triple jump = 675 px).
            # L tile sits on the first low platform, reachable with a single jump (216 px gap < 225 px max).
            # Exit 0 = top-left (loops back to start_hub)
            # Exit 1 = bottom-left (entry from dash_canyon)
            "levitate_ascent": Room(
                tile_map=[
                    "EEXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "E N                                        X",
                    "XXXXXXXXXXXXXXXXXXX                        X",
                    "X                                          X",
                    "X                          XXXXXXXXXXXXXXXX",
                    "X                                          X",
                    "X                                          X",
                    "X                                          X",
                    "X                                          X",
                    "X                      F                   X",
                    "X                                          X",
                    "X      P                                   X",
                    "XXXXXXXXXXXXXXXXXXXXXX                     X",
                    "X                                          X",
                    "X                                          X",
                    "X                                          X",
                    "X              F                           X",
                    "X                                          X",
                    "X                                          X",
                    "X                            P             X",
                    "X                     XXXXXXXXXXXXXXX      X",
                    "X                                          X",
                    "E N                                     L  X",
                    "E                                      XXX X",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                ],
            ),

            # --- Final room: placeholder win room — enter from levitate_ascent, exit to start_hub ---
            # W tile triggers the win condition; edit layout as needed
            "final_room": Room(
                tile_map=[
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "E            X                                                                       X                             X                                    E",
                    "EN     X     X                F                                                      X                      XXXX   X                   W            N   E",
                    "XXXXXXXX     X                F                                                      X                             X                   XXXXXXXXXXXXXXXXXX",
                    "X            X                  XXXXXXXX                                             X              XXXX           X            XXXXXXXX                X",
                    "X            X                F X      XXXXXXXXXXXX                                  X                             X                                    X",
                    "X        SSSSX                F X                 X                                  X                             X                                    X",
                    "X        XXXXX       XXXX                         X                                  X                             XXXXXXXXXXXXXXX                      X",
                    "XSSSS        X                      X             X                                  X        XXXX                                                      X",
                    "XXXXX        XXXX                   X             X                                  X                                     XXXX                         X",
                    "X               X                   X             X          XXXX                    X                                                                  X",
                    "XXXXXSSSSSXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   X                                                                                                     X",
                    "X                    X              X             X                           XX                                                                        X",
                    "XPPPPP                  X  P   X    P         X   XSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                ],
            ),

            # --- Room 6: vertical gauntlet — zigzag climb from left-bottom to right-top ---
            "vertical_gauntlet": Room(
                tile_map=[
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "X                                                     N E",
                    "X               F                                       E",
                    "X                          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "X                                                       X",
                    "X              P                                        X",
                    "X      XXXXXXXXXXXXXXXXXXXXX                        X   X",
                    "X                          X                        X   X",
                    "X                          X    XXXXXXXXXXXXXXXXXXXXX   X",
                    "X                          X                        X   X",
                    "X    XXXXXXXXXXXXXXXXXXXXXXX                            X",
                    "X                          XSSSS          P             X",
                    "X                          XXXXXXXXXXXXXXXXXXXXXXXXXX   X",
                    "X                                                       X",
                    "X          XXX                                          X",
                    "XSSSSSSSSSSSSSSSSSSSSSSSSSSXXXSSSSSXXXSSSSSXXSSSSXXS    X",
                    "XSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS    X",
                    "E N                                                     X",
                    "E                                                       X",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                ],
            ),
        }
        self.current_room_key = "start_hub"
        self.current_room = self.rooms[self.current_room_key]
        # --- Link exits ---
        # start_hub exit 0 = left side (return from levitate_ascent)
        # start_hub exit 1 = right side (forward to pit_room)
        self.link_bidirectional("start_hub", 1, "pit_room", 0, "right", "left")
        self.link_bidirectional("pit_room", 1, "vertical_climb", 0, "right", "left")
        self.link_bidirectional("vertical_climb", 1, "parkour", 0, "right", "left")
        self.link_bidirectional("parkour", 1, "spike_traverse", 0, "right", "left")
        self.link_bidirectional("spike_traverse", 1, "vertical_gauntlet", 1, "right", "left")
        # new rooms
        self.link_bidirectional("vertical_gauntlet", 0, "dash_canyon", 0, "right", "left")
        self.link_bidirectional("dash_canyon", 1, "levitate_ascent", 1, "right", "left")
        self.link_bidirectional("levitate_ascent", 0, "final_room", 0, "up", "left")
        self.link_bidirectional("final_room", 1, "start_hub", 0, "right", "down")

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

    def check_win_tile(self, player):
        """Returns True if the player is touching the W win tile in the current room."""
        player_rect = pygame.Rect(player.body.x, player.body.y, 20, 40)
        for rect in self.current_room.win_tiles:
            if player_rect.colliderect(rect):
                return True
        return False

    def check_skill_unlocks(self, player):
        """Grant a skill when the player touches its unlock tile, then remove the tile."""
        player_rect = pygame.Rect(player.body.x, player.body.y, 20, 40)
        for tile in self.current_room.unlock_tiles[:]:
            rect, skill = tile
            if player_rect.colliderect(rect):
                if skill == "dash":
                    player.has_dash = True
                elif skill == "levitate":
                    player.has_levitate = True
                self.current_room.unlock_tiles.remove(tile)

    def check_transitions(self, player):
        if self.transition_state != 'idle':
            return False
        if self.transition_cooldown > 0:
            self.transition_cooldown -= 1
            return False

        player_rect = pygame.Rect(player.body.x, player.body.y, 20, 40)

        for rect, target_room, spawn_pos, _, target_exit_index in self.current_room.exits:
            if player_rect.colliderect(rect):
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
