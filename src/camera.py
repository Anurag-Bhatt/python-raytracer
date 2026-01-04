import numpy as np
from hittable import Hittable
from interval import Interval
from utility import random_double, degrees_to_radians, random_range, normalise, cross, random_in_unit_disk
from math import inf, tan
from ray import Ray
from color import write_color



class Camera:

    def __init__(self, width=400, aspect_ratio=16/9, sample_per_pixel=10) -> None:
        self.aspect_ratio = aspect_ratio
        self.image_width = width

        self.image_height = int(self.image_width / self.aspect_ratio)
        self.image_height = self.image_height if self.image_height > 1 else 1
        
        # In Degrees, vertical field of view
        self.vfov = 90
        self.lookfrom       =   np.array([0.0, 0.0, 0.0], dtype=np.float32)       # Point Camera is looking from
        self.lookat         =   np.array([0.0, 0.0, -1.0], dtype=np.float32)      # Point Camera is looking at
        self.view_up        =   np.array([0.0, 1.0, 0.0], dtype=np.float32)         # Camera-relative up direction
                
        self.max_depth      = 10
        self.center         = np.zeros(3, dtype=np.float32)
        self.pixel00_loc    = np.zeros(3, dtype=np.float32)
        self.pixel_delta_u  = np.zeros(3, dtype=np.float32)
        self.pixel_delta_v  = np.zeros(3, dtype=np.float32)

        self.defocus_angle  = 0.0  # Variation angle of rays through each pixel
        self.focus_dist     = 10.0    # Distance from camera lookfrom point to plane of perfect focus

        self.defocus_disk_u = np.zeros(3, dtype=np.float32)
        self.defocus_disk_v = np.zeros(3, dtype=np.float32)

        self.sample_per_pixel = sample_per_pixel
        self.pixel_samples_scale:float = 1 / sample_per_pixel

    def render(self, world:Hittable, pixels):
        self.initialize()

        print("Starting Rendering...")
        print(f"Width:{self.image_width}, Height:{self.image_height}")

        for j in range(self.image_height):
            for i in range(self.image_width):

                pixel_color = np.zeros(3, dtype=np.float32)
                
                for sample in range(self.sample_per_pixel):
                    r:Ray = self.get_ray(i, j)
                    pixel_color += self.ray_color(r, self.max_depth, world)

                pixels[i, j] = write_color(pixel_color * self.pixel_samples_scale)
        
        print("Done")

    def initialize(self):

        self.center = self.lookfrom

        # Determine viewport dimensions
        #focal_length = (self.lookfrom - self.lookat).length()
        theta = degrees_to_radians(self.vfov)
        h = tan(theta/2.0)
        viewport_height = 2.0 * h * self.focus_dist
        viewport_width = viewport_height * (self.image_width / self.image_height)

        # Calculate the u,v,w unit basis vectors for the camera coordinate frame
        w = normalise(self.lookfrom - self.lookat)
        u = normalise(cross(self.view_up, w))
        v = cross(w, u)

        # Calculate the vectors across the horizontal and down the vertical viewport edges.
        viewport_u = viewport_width * u
        viewport_v = viewport_height * -v

        # Calculate the horizontal and vertical delta vectors from pixel to pixel
        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        # Calculate the location of the upper left pixel
        viewport_upper_left = self.center - (self.focus_dist * w) - viewport_u/2 - viewport_v/2
        self.pixel00_loc = viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)

        defocus_radius = self.focus_dist * tan(degrees_to_radians(self.defocus_angle / 2))
        self.defocus_disk_u = u * defocus_radius
        self.defocus_disk_v = v * defocus_radius

    @staticmethod
    def ray_color(r:Ray, depth:int, world:Hittable) -> np.ndarray:

        if depth <= 0:
            return np.zeros(3, dtype=np.float32)

        hit, rec = world.hit(r, Interval(0.001, inf))
        if hit == True and rec is not None:
            #direction = random_on_hemisphere(rec.normal)

            did_scatter, attenuation, scattered = rec.material.scatter(r, rec)
            if did_scatter:
                c = attenuation * Camera.ray_color(scattered, depth-1, world)
                #print(type(c.x), type(c))
                return c

            return np.zeros(3, dtype=np.float32)

        unit_direction = normalise(r.direction)
        a = 0.5 * (unit_direction[1] + 1.0)
        return (1.0-a)*np.array([1.0, 1.0, 1.0], dtype=np.float32) + a*np.array([0.5, 0.7, 1.0], dtype=np.float32)
    
    def get_ray(self, i:int, j:int):
        
        offset = self.sample_square()
        pixel_sample = self.pixel00_loc + ((i + offset[0]) * self.pixel_delta_u) + ((j + offset[1]) * self.pixel_delta_v)

        ray_origin = self.center if (self.defocus_angle <= 0) else self.defocus_disk_sample()
        ray_direction = pixel_sample - ray_origin

        return Ray(ray_origin, ray_direction)

    @staticmethod
    def sample_square():
        return np.array([random_double() - 0.5, random_double() - 0.5, 0], dtype=np.float32)
    
    def defocus_disk_sample(self):
        p = random_in_unit_disk()
        return self.center + (p[0] * self.defocus_disk_u) + (p[1] * self.defocus_disk_v)