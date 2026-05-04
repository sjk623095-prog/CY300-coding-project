import sys
import os
import pytest
import pygame

# This line ensures the project root is in the Python path so folders can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.player import Player
from world.level_manager import LevelManager

@pytest.fixture(autouse=True)
def setup_pygame():
    """Sets up a headless Pygame environment for testing logic without a window."""
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    yield
    pygame.quit()

def test_room_transition_logic():
    """
    Test 1: Verifies that the LevelManager correctly detects an exit overlap
    and initiates the transition state.
    """
    # Given: A LevelManager and a Player
    lm = LevelManager()
    player = Player(100, 100)
    
    # When: Manually place player inside the exit zone ('E') leading to pit_room
    # In start_hub, the exit to pit_room is at index 1 [cite: 1259]
    exit_rect = lm.rooms["start_hub"].exits[1][0]
    player.body.x = exit_rect.x + 5
    player.body.y = exit_rect.y + 5
    
    # Execute transition check
    triggered = lm.check_transitions(player)
    
    # Then: Assert the state has moved to fade_out and the correct room is pending [cite: 1260]
    assert triggered is True
    assert lm.transition_state == 'fade_out'
    assert lm._pending[0] == "pit_room"

def test_hazard_collision_reset():
    """
    Test 2: Verifies that touching an 'S' hazard tile correctly triggers 
    a player reset to a safe position.
    """
    # Given: A LevelManager and a Player at an arbitrary safe position
    lm = LevelManager()
    player = Player(0, 0)
    safe_pos = (300, 300)
    
    # When: Manually place player inside a hazard ('S') in the start_hub [cite: 1253]
    hazard_rect = lm.current_room.hazards[0]
    player.body.x = hazard_rect.x
    player.body.y = hazard_rect.y
    
    # Execute hazard check 
    was_reset = lm.check_hazards(player, safe_pos)
    
    # Then: Assert the reset occurred and the player's position/velocity updated
    assert was_reset is True
    assert player.body.x == safe_pos[0]
    assert player.body.y == safe_pos[1]
    assert player.body.vx == 0 and player.body.vy == 0