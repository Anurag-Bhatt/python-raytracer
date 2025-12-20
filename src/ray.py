from vec3 import Vec3

class Ray:

    def __init__(self, origin:Vec3, direction:Vec3) -> None:
        
        self.origin = origin
        self.direction = direction
    
    def at(self, t):
        return  self.origin + t * self.direction