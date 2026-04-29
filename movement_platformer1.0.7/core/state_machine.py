class StateMachine:
    """Generic finite state machine: holds the current state and drives enter/update/exit transitions."""

    def __init__(self, initial_state):
        self.current_state = initial_state
        self.current_state.enter()

    def change(self, new_state):
        self.current_state.exit()
        self.current_state = new_state
        self.current_state.enter()

    def update(self, player, dt):
        self.current_state.update(player, dt)

class PlayerState:
    """Base class for all player states; subclasses override update() to implement state logic."""

    def enter(self):
        pass

    def update(self, player, dt):
        pass

    def exit(self):
        pass

class IdleState(PlayerState):
    """Player is standing still on the ground; transitions to Run or Fall as conditions change."""

    def update(self, player, dt):
        if not player.on_ground:
            player.state_machine.change(FallState())

        elif abs(player.body.vx) > 50:
            player.state_machine.change(RunState())

class RunState(PlayerState):
    """Player is moving horizontally on the ground; transitions to Fall or Idle."""

    def update(self, player, dt):
        if not player.on_ground:
            player.state_machine.change(FallState())

        elif abs(player.body.vx) < 10:
            player.state_machine.change(IdleState())

class JumpState(PlayerState):
    """Player is moving upward after a jump; transitions to Fall when vertical velocity turns positive."""

    def enter(self):
        pass

    def update(self, player, dt):
        if player.body.vy > 0:
            player.state_machine.change(FallState())

class FallState(PlayerState):
    """Player is falling; can enter WallSlide if touching a wall, or land to Idle/Run."""

    def update(self, player, dt):

        if player.on_wall and not player.on_ground:
            if not isinstance(player.state_machine.current_state, WallSlideState):
                player.state_machine.change(WallSlideState())
            return

        if player.on_ground:
            if abs(player.body.vx) > 50:
                player.state_machine.change(RunState())
            else:
                player.state_machine.change(IdleState())

class WallSlideState(PlayerState):
    """Player is pressed against a wall mid-air; caps fall speed and allows a wall-jump."""

    def update(self, player, dt):

        # slow falling
        if player.body.vy > 0:
            player.body.vy = min(player.body.vy, 200)

        # leave wall
        if not player.on_wall:
            player.state_machine.change(FallState())

        # hit ground
        elif player.on_ground:
            player.state_machine.change(IdleState())
