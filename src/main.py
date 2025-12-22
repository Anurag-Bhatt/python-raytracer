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

def ray_color(r:Ray, world:Hittable):

    hit, rec = (world.hit(r, Interval(0.0, inf)))
    if hit and rec is not None:
        return 0.5 * (rec.normal + color(1, 1, 1))
    
    unit_direction:Vec3 = unit_vector(r.direction)
    a = 0.5 * (unit_direction.y + 1.0)
    return (1.0-a)*color(1.0, 1.0, 1.0) + a*color(0.5, 0.7, 1.0)


def main():
    
    world = HittableList()

    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(0, -100.5, -2), 100))
    
    aspect_ratio = 16.0 / 9.0
    image_width:int = 400
    cam = Camera()
    cam.aspect_ratio = aspect_ratio
    cam.image_width = image_width

    im = Image.new("RGB", (cam.image_width, cam.image_height))
    pixels= im.load()
    
    cam.render(world, pixels)
    
    im.show()

main()