from math import sqrt
from vec3 import Vec3
from interval import Interval
Color = Vec3

INTENSITY = Interval(0.000, 0.999)

def linear_to_gamma(linear_component:float):

    if linear_component > 0:
        return sqrt(linear_component)
    
    return 0
    

def write_color(pixel_color: Color) -> tuple[int, int, int]:
    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z

    r = linear_to_gamma(r)
    g = linear_to_gamma(g)
    b = linear_to_gamma(b)

    rbyte = int(256 * INTENSITY.clamp(r))
    gbyte = int(256 * INTENSITY.clamp(g))
    bbyte = int(256 * INTENSITY.clamp(b))

    return rbyte, gbyte, bbyte