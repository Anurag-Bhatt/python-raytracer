import numpy as np
from hittable import Hittable
from utility import random_double, degrees_to_radians, normalise, cross
from ray import Ray

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

        accumulated_colors = np.zeros((self.image_height, self.image_width, 3), dtype=np.float32)

        j, i = np.meshgrid(np.arange(self.image_height), np.arange(self.image_width), indexing="ij")
        for s in range(self.sample_per_pixel):    
            offsets = np.random.uniform(-0.5, 0.5, (self.image_height, self.image_width, 2))

            pixel_sample = (
                self.pixel00_loc + 
                (i[..., None] + offsets[..., 0:1]) * self.pixel_delta_u +
                (j[..., None] + offsets[..., 1:2]) * self.pixel_delta_v
            )

            
            if self.defocus_angle <= 0:
                ray_origins = np.broadcast_to(self.center, pixel_sample.shape)
            else:
                ray_origins = self.defocus_disk_sample()

            ray_directions = pixel_sample - ray_origins
            rays = Ray(ray_origins, ray_directions)

            sample_color = self.ray_color(rays, world, self.max_depth)
            accumulated_colors += sample_color
        
        final_colors =  accumulated_colors / self.sample_per_pixel
        final_colors =  np.sqrt(np.maximum(0, final_colors))
        
        final_colors = (np.clip(final_colors, 0.0, 0.999) * 255.99).astype(np.uint8)

        return final_colors

    def initialize(self):

        self.center = self.lookfrom

        # Determine viewport dimensions
        #focal_length = (self.lookfrom - self.lookat).length()
        theta = degrees_to_radians(self.vfov)
        h = np.tan(theta/2.0)
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

        defocus_radius = self.focus_dist * np.tan(degrees_to_radians(self.defocus_angle / 2))
        self.defocus_disk_u = u * defocus_radius
        self.defocus_disk_v = v * defocus_radius

    
    def ray_color(self, rays, world, depth) -> np.ndarray:
        attenuation = np.ones((self.image_height, self.image_width, 3), dtype=np.float32)
        final_color = np.zeros((self.image_height, self.image_width, 3), dtype=np.float32)
        active_mask = np.ones((self.image_height, self.image_width), dtype=bool)

        for bounce in range(depth):
            hit_mask, t_values, obj_indices = world.hit(rays, 0.001, np.inf)

            miss_mask = active_mask & ~hit_mask
            if np.any(miss_mask):
                unit_dirs = rays.direction / np.linalg.norm(rays.direction, axis=-1, keepdims=True)
                a = 0.5 * (unit_dirs[..., 1] + 1.0)
                sky_color = (1.0 - a)[..., None] * np.array([1.0, 1.0, 1.0]) + a[..., None] * np.array([0.5, 0.7, 1.0])

                final_color[miss_mask] += attenuation[miss_mask] * sky_color[miss_mask]
                active_mask[miss_mask] = False

            if not np.any(active_mask):
                break

            points, normals, front_faces = world.get_world_record(rays, hit_mask, t_values, obj_indices)

            for idx, obj in enumerate(world.objects):
                mat_mask = hit_mask & (obj_indices == idx)

                if np.any(mat_mask):
                    new_dirs, mat_albedo = obj.mat.scatter_batch(
                        rays, points, normals, front_faces, mat_mask
                    )

                    rays.origin[mat_mask] = points[mat_mask]
                    rays.direction[mat_mask] = new_dirs
                    attenuation[mat_mask] *= mat_albedo

        return final_color

    @staticmethod
    def sample_square():
        return np.array([random_double() - 0.5, random_double() - 0.5, 0], dtype=np.float32)
    
    def defocus_disk_sample(self):
        shape = (self.image_height, self.image_width)
        p = random_unit_disk_vectorized(shape)

        offsets = (p[..., 0:1] * self.defocus_disk_u) + (p[..., 1:2] * self.defocus_disk_v)
        return self.center + offsets

def random_unit_disk_vectorized(shape):
    """Returns an array of shape (*shape, 3) with random poitns in a unit disk."""

    r = np.sqrt(np.random.uniform(0, 1, shape))
    theta = np.random.uniform(0, 2 * np.pi, shape)

    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.zeros_like(x)

    return np.stack([x, y, z], axis=-1)