import cProfile, pstats, re
from PIL import Image

import numpy as np

from utility import random_vec3, random_vec3_range
from sphere import Sphere
from hittable_list import HittableList
from camera import Camera
import material

print("Raytracing")

def main():
    
    world = HittableList()

    ground_material = material.Lambertian(np.array([0.5, 0.5, 0.5], dtype=np.float32))
    world.add(Sphere(np.array([0, -1000, 0], dtype=np.float32), 1000, ground_material))

    for a in range(-1, 1):
        for b in range(-1, 1):

            choose_mat = np.random.uniform()
            center = np.array([a + 0.9*np.random.uniform(), 0.2, b + 0.9*np.random.uniform()], dtype=np.float32)

            if (np.linalg.norm(center - np.array([4.0, 0.2, 0.0], dtype=np.float32)) > 0.9):
                sphere_material:material.Material

                if choose_mat < 0.8:
                    # Diffuse
                    albedo = random_vec3() * random_vec3()
                    sphere_material = material.Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                
                elif choose_mat < 0.95:
                    # Metal
                    albedo = random_vec3_range(0.5, 1)
                    fuzz = np.random.uniform(0, 0.5)
                    sphere_material = material.Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    # Glass
                    sphere_material = material.Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))


    material_1 = material.Dielectric(1.5)
    world.add(Sphere(np.array([0,1,0], dtype=np.float32), 1.0, material_1))

    material_2 = material.Lambertian(np.array([0.4, 0.2, 0.1], np.float32))
    world.add(Sphere(np.array([-4, 1, 0], dtype=np.float32), 1.0, material_2))

    material_3 = material.Metal(np.array([0.7, 0.6, 0.5], dtype=np.float32), 0.0)
    world.add(Sphere(np.array([4, 1, 0], dtype=np.float32), 1.0, material_3))

    cam = Camera(width=400, aspect_ratio=16.0/9.0, sample_per_pixel=10)

    cam.vfov = 20
    cam.lookfrom = np.array([13, 2, 1], dtype=np.float32)
    cam.lookat = np.array([0, 0, -1], dtype=np.float32)
    cam.view_up = np.array([0, 1, 0], dtype=np.float32)

    cam.defocus_angle = 0.6
    cam.focus_dist = 10.0

    cam.initialize()

    im = Image.new("RGB", (cam.image_width, cam.image_height))
    pixels= im.load()
    
    colors = cam.render(world, pixels)
    
    im = Image.fromarray(colors)

    im.show()

    im.save("images/test_render_5.png")

if __name__ == '__main__':
    
    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats(pstats.SortKey.CUMULATIVE)
    stats.dump_stats("data.prof")