from hittable import Hittable
from vec3 import Vec3, unit_vector
from interval import Interval
from math import inf
from ray import Ray
from color import write_color

Point3 = Vec3
color = Vec3

class Camera:

    def __init__(self, width=400, aspect_ratio=16/9) -> None:
        self.aspect_ratio = aspect_ratio
        self.image_width = width

        self.image_height = int(self.image_width / self.aspect_ratio)
        self.image_height = self.image_height if self.image_height > 1 else 1
        
        self.center = Vec3(0, 0, 0)
        self.pixel00_loc = Vec3(0, 0, 0)
        self.pixel_delta_u = Vec3(0, 0, 0)
        self.pixel_delta_v = Vec3(0, 0, 0)

    def render(self, world:Hittable, pixels):
        self.initialize()

        print("Starting Rendering...")
        print(f"Width:{self.image_width}, Height:{self.image_height}")

        for j in range(self.image_height):
            for i in range(self.image_width):

                pixel_center = self.pixel00_loc + (i * self.pixel_delta_u) + (j * self.pixel_delta_v)
                ray_direction = pixel_center - self.center
                r = Ray(self.center, ray_direction)

                pixel_color = self.ray_color(r, world)
                pixels[i, j] = write_color(pixel_color)
        
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


    def ray_color(self, r:Ray, world:Hittable):
        hit, rec = world.hit(r, Interval(0.001, inf))
        if hit == True and rec is not None:
            return 0.5 * (rec.normal + color(1, 1, 1))

        unit_direction:Vec3 = unit_vector(r.direction)
        a = 0.5 * (unit_direction.y + 1.0)
        return (1.0-a)*color(1.0, 1.0, 1.0) + a*color(0.5, 0.7, 1.0)