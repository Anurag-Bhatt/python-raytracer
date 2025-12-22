# pyright: reportOptionalSubscript=false
from PIL import Image
from math import sqrt, pi, inf

from interval import Interval
from vec3 import Vec3, unit_vector, dot
from ray import Ray
from color import write_color
from sphere import Sphere
from hittable_list import HittableList
from hittable import Hittable
from camera import Camera

print("Raytracing")

color = Vec3
Point3 = Vec3

# Utility Functions
def degrees_to_radians(degree:float):
    return degree * pi / 180

def main():
    
    world = HittableList()

    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(0, -100.5, -1), 100))
    
    cam = Camera(width=400, aspect_ratio=16.0/9.0)
    cam.initialize()

    im = Image.new("RGB", (cam.image_width, cam.image_height))
    pixels= im.load()
    
    cam.render(world, pixels)
    
    im.show()

main()