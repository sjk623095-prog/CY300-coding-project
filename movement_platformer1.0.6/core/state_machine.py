class StateMachine:
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
    def enter(self):
        pass

    def update(self, player, dt):
        pass

    def exit(self):
        pass

class IdleState(PlayerState):
    def update(self, player, dt):
        if not player.on_ground:
            player.state_machine.change(FallState())

        elif abs(player.body.vx) > 50:
            player.state_machine.change(RunState())

class RunState(PlayerState):
    def update(self, player, dt):
        if not player.on_ground:
            player.state_machine.change(FallState())

        elif abs(player.body.vx) < 10:
            player.state_machine.change(IdleState())

class JumpState(PlayerState):
    def enter(self):
        pass

    def update(self, player, dt):
        if player.body.vy > 0:
            player.state_machine.change(FallState())

class FallState(PlayerState):
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
