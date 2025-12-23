from hittable import Hittable
from vec3 import Vec3, unit_vector, random_on_hemisphere
from interval import Interval
from utility import random_double
from math import inf
from ray import Ray
from color import write_color

Point3 = Vec3
color = Vec3

class Camera:

    def __init__(self, width=400, aspect_ratio=16/9, sample_per_pixel=10) -> None:
        self.aspect_ratio = aspect_ratio
        self.image_width = width

        self.image_height = int(self.image_width / self.aspect_ratio)
        self.image_height = self.image_height if self.image_height > 1 else 1
        
        self.max_depth = 10
        self.center = Vec3(0, 0, 0)
        self.pixel00_loc = Vec3(0, 0, 0)
        self.pixel_delta_u = Vec3(0, 0, 0)
        self.pixel_delta_v = Vec3(0, 0, 0)

        self.sample_per_pixel = sample_per_pixel
        self.pixel_samples_scale:float = 1 / sample_per_pixel

    def render(self, world:Hittable, pixels):
        self.initialize()

        print("Starting Rendering...")
        print(f"Width:{self.image_width}, Height:{self.image_height}")

        for j in range(self.image_height):
            for i in range(self.image_width):

                pixel_color:color = color(0,0,0)
                
                for sample in range(self.sample_per_pixel):
                    r:Ray = self.get_ray(i, j)
                    pixel_color += self.ray_color(r, self.max_depth, world)


                pixels[i, j] = write_color(pixel_color * self.pixel_samples_scale)
        
        print("Done")

    def initialize(self):
        focal_length = 1.0
        viewport_height = 2.0
        viewport_width = viewport_height * (self.image_width / self.image_height)

        viewport_u = Vec3(viewport_width, 0, 0)
        viewport_v = Vec3(0, -viewport_height, 0)

        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        viewport_upper_left = self.center - Vec3(0, 0, focal_length) - viewport_u/2 - viewport_v/2
        self.pixel00_loc = viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)

    @staticmethod
    def ray_color(r:Ray, depth:int, world:Hittable):

        if depth <= 0:
            return color(0, 0, 0)

        hit, rec = world.hit(r, Interval(0.001, inf))
        if hit == True and rec is not None:
            direction = random_on_hemisphere(rec.normal)
            return 0.5 * Camera.ray_color(Ray(rec.p, direction), depth-1, world)

        unit_direction:Vec3 = unit_vector(r.direction)
        a = 0.5 * (unit_direction.y + 1.0)
        return (1.0-a)*color(1.0, 1.0, 1.0) + a*color(0.5, 0.7, 1.0)
    
    def get_ray(self, i:int, j:int):
        
        offset = self.sample_square()
        pixel_sample = self.pixel00_loc + ((i + offset.x) * self.pixel_delta_u) + ((j + offset.y) * self.pixel_delta_v)

        ray_origin = self.center
        ray_direction = pixel_sample - ray_origin

        return Ray(ray_origin, ray_direction)

    @staticmethod
    def sample_square():
        return Vec3(random_double() - 0.5, random_double() - 0.5, 0)