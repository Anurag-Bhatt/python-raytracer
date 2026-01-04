from __future__ import annotations
import numpy as np
from utility import random_double, random_range

class Vec3:

    @classmethod
    def fromArray(cls, arr):
        return cls(arr[0], arr[1], arr[2])

    def __init__(self, x:float, y:float, z:float): 
        self.axis = np.array([x,y,z],dtype=np.float32)
        
    def __add__(self, other:Vec3) -> Vec3:
        return Vec3.fromArray(self.axis + other.axis)
    
    def __sub__(self, other:Vec3) -> Vec3:
        return Vec3.fromArray(self.axis - other.axis)

    def __mul__(self, other) -> Vec3:
        if isinstance(other, Vec3):
            return Vec3.fromArray(self.axis * other.axis)
        else:
            return Vec3.fromArray(self.axis * other)

    def __rmul__(self, other) -> Vec3:
        return self * other

    def __truediv__(self, other) -> Vec3:
        return Vec3.fromArray(self.axis / other)
    
    def __neg__(self)->Vec3:
        return Vec3.fromArray(-self.axis)

    def __repr__(self) -> str:
        return f"Vec3({self.axis[0]:0.4}, {self.axis[1]:0.4}, {self.axis[2]:0.4})"

    def length_squared(self)->float:
        return float(np.dot(self.axis, self.axis))
    
    def length(self)->float:
        return float(np.sqrt(self.length_squared()))
    
    # Returns true if the vector is close to zero in all three dimensions
    def near_zero(self):
        s = 1e-8
        return np.all(np.abs(self.axis) < s)

    @staticmethod
    def random_vec3():
        return Vec3(random_double(), random_double(), random_double())
    
    @staticmethod
    def random_vec3_range(min, max):
        return Vec3(random_range(min, max), random_range(min, max), random_range(min, max))
    
def dot(u:Vec3, v:Vec3)->float:
    return float(np.dot(u.axis,v.axis))

def cross(u:Vec3, v:Vec3)->Vec3:
    return Vec3.fromArray(np.cross(u.axis, v.axis))

def unit_vector(u:Vec3)->Vec3:
    length_sqr = u.length_squared()
    if length_sqr < 1e-16:
        return Vec3(0.0, 0.0, 0.0)
    
    return Vec3.fromArray(u.axis / np.sqrt(length_sqr))

def random_unit_vector()->Vec3:
    while(True):
        p = Vec3.random_vec3_range(-1, 1)
        length_sqr = p.length_squared()
        if 1e-8 < length_sqr <= 1:
            return p/(np.sqrt(length_sqr))
            
# Creates a unit vector on a unit sphere and checks for the angle between the normal and itself
def random_on_hemisphere(normal:Vec3)->Vec3:
    on_unit_sphere = random_unit_vector()
    if dot(on_unit_sphere, normal) > 0.0:
        return on_unit_sphere
    else:
        return -on_unit_sphere

# Finds a random point on the a disk of unit radius
def random_in_unit_disk()->np.ndarray:
    while True:
        p = np.array([random_range(-1, 1), random_range(-1, 1), 0], dtype=np.float32)
        if np.dot(p, p) < 1:
            return p

# Reflects the vector V using vector maths
def reflect(v:Vec3, n:Vec3):
    return v - 2*dot(v,n)*n

# Refraction for dielectric materials
def refract(v:Vec3, n:Vec3, etai_over_etat):
    
    cos_theta = min(dot(-v, n), 1)
    r_out_perp:Vec3 = etai_over_etat * (v + cos_theta * n)
    r_out_para:Vec3 = -np.sqrt(np.abs(1.0 - r_out_perp.length_squared())) * n

    return r_out_perp + r_out_para