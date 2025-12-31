from PIL import Image
from math import sqrt, pi, inf, cos

from vec3 import Vec3, random_double, random_range
from sphere import Sphere
from hittable_list import HittableList
from camera import Camera
import material

print("Raytracing")

color = Vec3
Point3 = Vec3

def main():
    
    world = HittableList()

    ground_material = material.Lambertian(color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):

            choose_mat = random_double()
            center:Point3 = Point3(a + 0.9*random_double(), 0.2, b + 0.9*random_double())

            if ((center - Point3(4, 0.2, 0)).length() > 0.9):
                sphere_material:material.Material

                if choose_mat < 0.8:
                    # Diffuse
                    albedo = color.random_vec3() * color.random_vec3()
                    sphere_material = material.Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                
                elif choose_mat < 0.95:
                    # Metal
                    albedo = color.random_vec3_range(0.5, 1)
                    fuzz = random_range(0, 0.5)
                    sphere_material = material.Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    # Glass
                    sphere_material = material.Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))


    material_1 = material.Dielectric(1.5)
    world.add(Sphere(Point3(0,1,0), 1.0, material_1))

    material_2 = material.Lambertian(color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4, 1, 0), 1.0, material_2))

    material_3 = material.Metal(color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(Point3(4, 1, 0), 1.0, material_3))

    cam = Camera(width=400, aspect_ratio=16.0/9.0, sample_per_pixel=10)

    cam.vfov = 20
    cam.lookfrom = Point3(13, 2, 1)
    cam.lookat = Point3(0, 0, -1)
    cam.view_up = Vec3(0, 1, 0)

    cam.defocus_angle = 0.6
    cam.focus_dist = 10.0

    cam.initialize()

    im = Image.new("RGB", (cam.image_width, cam.image_height))
    pixels= im.load()
    
    cam.render(world, pixels)
    
    im.show()

    im.save("images/final_render.png")

main()