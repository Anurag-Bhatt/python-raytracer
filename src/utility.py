from math import pi
import random

# Utility Functions
def degrees_to_radians(degree:float):
    return degree * pi / 180

def random_double() -> float:
    return random.random()

def random_range(min_val:float, max_val:float) -> float:
    return min_val + (max_val - min_val) * random.random()
