from PIL import Image
from math import sqrt, pi, inf

from vec3 import Vec3
from sphere import Sphere
from hittable_list import HittableList
from camera import Camera
import material

print("Raytracing")

color = Vec3
Point3 = Vec3

def main():
    
    world = HittableList()

    material_ground  = material.Lambertian(color(0.8, 0.8, 0.0))
    material_center  = material.Lambertian(color(0.1, 0.2, 0.5))
    material_left    = material.Metal(color(0.8, 0.8, 0.8))
    material_right   = material.Metal(color(0.8, 0.6, 0.2))

    world.add(Sphere(Point3(0, -100.5, -1), 100, material_ground))
    world.add(Sphere(Point3(0, 0, -1.2), 0.5, material_center))
    world.add(Sphere(Point3(-1, 0, -1), 0.5, material_left))
    world.add(Sphere(Point3(1, 0, -1), 0.5, material_right))
    
    cam = Camera(width=400, aspect_ratio=16.0/9.0, sample_per_pixel=10)
    cam.initialize()

    im = Image.new("RGB", (cam.image_width, cam.image_height))
    pixels= im.load()
    
    cam.render(world, pixels)
    
    im.show()

    im.save("images/diffuse_sphere.png")

main()
