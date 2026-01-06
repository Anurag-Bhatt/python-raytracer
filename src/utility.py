import random
import numpy as np

# Utility Functions
def degrees_to_radians(degree:float):
    return degree * np.pi / 180

def random_double() -> float:
    return random.random()

def random_range(min_val:float, max_val:float) -> float:
    return min_val + (max_val - min_val) * random.random()

def random_unit_vector()->np.ndarray:
    while(True):
        p = np.array([random_range(-1, 1), random_range(-1, 1), random_range(-1, 1)], dtype=np.float32)
        length_sqr = np.dot(p, p)
        if 1e-8 < length_sqr <= 1:
            return p/(np.sqrt(length_sqr))

# Helper functions
def normalise(v:np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    
    return v / norm

def cross(v:np.ndarray, u:np.ndarray) -> np.ndarray:
    return np.cross(v, u)

def near_zero(u:np.ndarray):
        s = 1e-8
        return np.all(np.abs(u) < s)

# Finds a random point on the a disk of unit radius
def random_in_unit_disk()->np.ndarray:
    while True:
        p = np.array([random_range(-1, 1), random_range(-1, 1), 0], dtype=np.float32)
        if np.dot(p, p) < 1:
            return p

def random_vec3():
        return np.array([random_double(), random_double(), random_double()], dtype=np.float32)

def random_vec3_range(min, max):
        return np.array([random_range(min, max), random_range(min, max), random_range(min, max)], dtype=np.float32)

def random_unit_vector_batch(n):
  
    z = np.random.uniform(-1, 1, n)
    phi = np.random.uniform(0, 2 * np.pi, n)
    
    # Convert to Cartesian
    r = np.sqrt(np.maximum(0, 1 - z**2))
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    
    return np.stack([x, y, z], axis=-1)