from __future__ import annotations

import numpy as np

from hittable import Hittable
from material import Material

class Sphere(Hittable):

    def __init__(self, center:np.ndarray, radius:float, mat:Material) -> None:

        self.center = center
        self.radius = radius
        self.mat = mat
    
    def hit(self, rays, t_min:float, t_max:float):
        
        oc = rays.origin - self.center

        a = np.sum(rays.direction**2, axis=-1)
        h = np.sum(oc*rays.direction, axis=-1)
        c = np.sum(oc*oc, axis=-1) - (self.radius**2)

        discriminant = h**2 - a*c

        hit_mask = discriminant > 0
        sqrt_d = np.sqrt(np.maximum(0, discriminant))

        root = (-h - sqrt_d)/a
        hit_mask = hit_mask & (root > t_min) & (root < t_max)
        t_values = np.where(hit_mask, root, np.inf)

        obj_ids = np.where(hit_mask, 0, -1)
        
        return hit_mask, t_values, obj_ids
    
    def get_record(self, rays, t_values, hitmask):

        points = rays.origin[hitmask] + t_values[hitmask, np.newaxis] * rays.direction[hitmask]

        outward_normals = (points - self.center) / self.radius

        direction = rays.direction[hitmask]
        front_faces = np.sum(direction * outward_normals, axis=1) < 0

        normals = np.where(front_faces[..., np.newaxis], outward_normals, -outward_normals)

        return points, normals, front_faces 