from settings import GRAVITY

class PhysicsBody1:
    """2D physics body storing position, velocity, and acceleration; supports gravity and force application."""

    def __init__(self,x,y):
        #Position
        self.x = float(x)
        self.y = float(y)

        #Velocity
        self.vx = 0.0
        self.vy = 0.0

        #Acceleration
        self.ax = 0.0
        self.ay = 0.0

        #Physics Properties
        self.mass = 1.0
        self.use_gravity = True
        #limit
        self.max_fall_speed = 2000

    def apply_force(self, fx, fy):
        self.ax += fx/ self.mass
        self.ay += fy / self.mass
    
    def apply_gravity(self):
        if self.use_gravity:
            self.ay += GRAVITY

    def integrate(self,dt):
        """Euler integration"""

        #update vel from acc
        self.vx += self.ax * dt
        self.vy += self.ay * dt


        #update pos from vel
        self.x += self.vx * dt
        self.y += self.vy * dt

        #clamp fall speed
        if self.vy > self.max_fall_speed:
            self.vy = self.max_fall_speed

        #reset forces
        self.ax = 0.0
        self.ay = 0.0

#later includes:
"""
apply_gravity()
apply_force()
integrate(dt)
"""