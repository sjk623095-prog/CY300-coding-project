Project Overview:
  A 2D sci-fi space platformer built with Python and pygame. The player navigates a series
  of 9 interconnected rooms, each defined by a tile-map, using physics-based movement that
  includes acceleration, friction, gravity, double-jump, and wall-sliding. Two unlockable
  skills -- Dash (triggered by right-click) and Levitate (triggered by left-click) -- are
  inside specific rooms and must be collected to progress through later, more demanding
  levels. Enemies (ground-patrolling and airborne) chase the player on detection. Hazard tiles
  (spikes) deal damage and reset the player to the last safe ground position. The player has
  5 lives; losing all lives resets the entire game. Room transitions use a fade-to-black
  effect. A HUD displays remaining lives and which skills have been unlocked.

Explanation of Files:
  main.py
    Entry point. Instantiates the Game object and calls game.run() to start the main loop.

  settings.py
    Global constants shared across all modules: SCREEN_WIDTH (1280), SCREEN_HEIGHT (720),
    FPS (60), and GRAVITY (1800 px/s^2).

  requirements.txt
    Lists the single external dependency: pygame >= 2.0.0.

  core/game.py
    The Game class. Owns the pygame window, clock, physics engine, camera, player, and
    LevelManager. The main loop calls handle_events(), update(), and draw() every frame.
    update() applies physics, resolves collisions, checks room transitions, hazards, skill
    unlocks, and enemy contact. draw() renders the room, player, HUD, and the fade overlay.
    reset_game() fully restores initial state when the player runs out of lives.

  core/player.py
    The Player class. Wraps a PhysicsBody1 and a StateMachine. Each frame it reads keyboard
    input (A/D to move, Space to jump) and mouse buttons (RMB = Dash, LMB = Levitate).
    Horizontal movement uses acceleration (3000 px/s^2) and ground friction (8000 px/s^2)
    capped at 800 px/s. Double-jump allows two jumps before landing; wall-sliding caps
    downward speed at 200 px/s and enables a wall-jump. Dash overrides horizontal velocity
    to 1400 px/s for 0.18 s with a 0.8 s cooldown. Levitate caps fall speed at 150 px/s
    while the button is held (1.2 s cooldown). take_damage() applies a 2-second invincibility
    window and knockback on hit.

  core/camera.py
    The Camera class. Smoothly lerps its offset toward the player each frame (factor 10*dt)
    to keep the player centered. Supports a zoom level that scales all world-to-screen
    conversions via apply() and apply_pos(). Zoom is animated dynamically in game.py
    (zooms out when the player falls fast).

  core/state_machine.py
    A generic StateMachine with enter/update/exit lifecycle methods, and five concrete
    PlayerState subclasses: IdleState, RunState, JumpState, FallState, and WallSlideState.
    States transition automatically based on on_ground, on_wall, and velocity thresholds.

  physics/physics_body.py
    PhysicsBody1. Stores float position (x, y), velocity (vx, vy), and acceleration (ax, ay).
    apply_gravity() adds GRAVITY to ay each step. integrate(dt) advances velocity then
    position using Euler integration and clamps vy to max_fall_speed (2000 px/s). Forces
    are zeroed after each integration step.

  physics/physics_engine.py
    physics_engine_1. Holds a list of PhysicsBody1 objects. Each call to step(dt) applies
    gravity to every body, integrates vertical velocity, and clamps fall speed. Horizontal
    position integration is performed separately in game.py to allow X and Y collision
    resolution to be interleaved.

  physics/collision_handler.py
    resolve_collisions_x() and resolve_collisions_y(). Each function constructs a 20x40
    AABB for the player, iterates over room platforms, and pushes the player out of any
    overlap. X resolution sets on_wall and wall_dir; Y resolution sets on_ground and zeroes
    vertical velocity on landing or ceiling hits.

  world/roomex.py
    The Room class. Parses a list of tile-map strings at construction time. Character
    meanings: X = solid platform, S = spike hazard, E = exit zone, N = spawn marker,
    P = PatrolEnemy, F = FlyingEnemy, D = dash unlock tile, L = levitate unlock tile, W = win condition.
    build_exit_zones() flood-fills adjacent E tiles into a single exit rectangle.
    _match_start_points() pairs each exit zone with the nearest N tile as its spawn
    position. update() ticks every enemy and removes any that touch a hazard. draw()
    renders platforms, hazards, exit outlines, unlock tiles, and enemies through the camera.

  world/level_manager.py
    The LevelManager class. Defines all 9 rooms (start_hub, pit_room, vertical_climb,
    parkour, spike_traverse, vertical_gauntlet, dash_canyon, levitate_ascent, final_room) and links
    their exits bidirectionally. check_transitions() detects player overlap with an exit
    zone and initiates a fade-to-black transition. update_transition() advances the
    fade_out -> room swap -> fade_in sequence. check_hazards() resets the player to the
    last safe ground position and returns True so game.py can deduct a life.
    check_skill_unlocks() grants the corresponding ability when the player touches a D or
    L tile and removes it from the room.

  enemies/enemies.py
    EnemyBase, PatrolEnemy, and FlyingEnemy, each driven by an EnemyStateMachine.
    PatrolEnemy (red, 24x40) walks at 120 px/s, reverses at walls or ledge edges, and
    chases at 220 px/s when the player enters 300 px detection range. FlyingEnemy
    (purple, 28x28) ignores gravity, bobs sinusoidally in HoverState, and homes in on the
    player at 200 px/s via normalized direction vectors in ChaseAirState (400 px detection
    range). Both share _resolve_x/_resolve_y for collision and touches_hazard() which lets
    the room remove enemies that fall onto spike tiles.

Run Instructions:
  Prerequisites:
    Python 3.10 or later
    pygame 2.0.0 or later

  1. Open a terminal and navigate to the movement_platformer1.0.6 directory.

  2. Install dependencies:
       pip install -r requirements.txt

  3. Run the game:
       python main.py

  Controls:
    A / D         Move left / right
    Space         Jump (up to 2 jumps before landing; wall-jump when against a wall)
    Right-click   Dash (requires Dash skill -- collect the orange tile in dash_canyon)
    Left-click    Levitate / slow fall (requires Levitate skill -- collect the cyan tile
                  in levitate_ascent)
    ESC           Quit

  Notes:
    - The window is resizable; the camera and zoom adjust automatically.
    - All 9 rooms form a loop. Completing final_room returns the player to start_hub.
    - Lives remaining and unlocked skills are shown in the top-left HUD.
