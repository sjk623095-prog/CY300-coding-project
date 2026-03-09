class PhysicsBody1:
    def __init__(self,x,y):
        self.x = x
        self.y = y

        self.vx = 0
        self.vy = 0

        self.ax = 0
        self.ay = 0

#later includes:
"""
apply_gravity()
apply_force()
integrate(dt)
"""