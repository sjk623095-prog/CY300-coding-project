

class physics_engine_1:
    def __init__(self):
        self.bodies = []
        
    def add_body(self, body):
        self.bodies.append(body)

    def step(self,dt):
        for body in self.bodies:

            if body.use_gravity:
                body.apply_gravity()


            body.vy += body.ay * dt
            body.ay = 0

            if body.vy > body.max_fall_speed:
                body.vy = body.max_fall_speed
