import math 
from utility import random_double, random_range

class Vec3:
    def __init__(self, x, y, z):
        
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vec3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return Vec3(self.x / other, self.y / other, self.z / other)
    
    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __repr__(self) -> str:
        return f"x:{self.x}, y:{self.y}, z:{self.z}"

    def length_squared(self):
        return (self.x * self.x + self.y * self.y + self.z * self.z)
    
    def length(self):
        return math.sqrt(self.length_squared())
    
    def near_zero(self):
        # Returns true if the vector is close to zero in all three dimensions
        s = 1e-8
        return abs(self.x) < s and abs(self.y) < s and abs(self.z) < s

    @staticmethod
    def random_vec3():
        return Vec3(random_double(), random_double(), random_double())
    
    @staticmethod
    def random_vec3_range(min, max):
        return Vec3(random_range(min, max), random_range(min, max), random_range(min, max))
    
   
    

def dot(u, v):
    return u.x * v.x +  u.y * v.y + u.z * v.z

def cross(u, v):
    return Vec3(
        u.y * v.z - u.z * v.y,
        u.z * v.x - u.x * v.z,
        u.x * v.y - u.y * v.x,
    )

def unit_vector(u):
    return u / u.length()

def random_unit_vector():
    while(True):
        p = Vec3.random_vec3_range(-1, 1)
        lensq = p.length_squared()
        if 1e-160 < lensq and lensq <= 1:
            return p/p.length()
            
# Creates a unit vector on a unit sphere and checks for the angle between the normal and itself
def random_on_hemisphere(normal:Vec3):
    on_unit_sphere = random_unit_vector()
    if dot(on_unit_sphere, normal) > 0.0:
        return on_unit_sphere
    else:
        return -on_unit_sphere
    
# Reflects the vector V using vector maths
def reflect(v:Vec3, n:Vec3):
    return v - 2*dot(v,n)*n