from __future__ import annotations
from abc import ABC, abstractmethod

import numpy as np

from utility import random_unit_vector_batch

class Material(ABC):
    @abstractmethod
    def scatter_batch(self, rays_in, points, normals, front_faces, mask) -> tuple[np.ndarray, np.ndarray]:
        """
        Returns:
            (scattered_rays, attenuation_mask)
        """
        pass

class Lambertian(Material):

    def __init__(self, albedo:np.ndarray) -> None:
        self.albedo = albedo

    def scatter_batch(self, rays_in, points, normals, front_faces, mask):

        num_hits = np.count_nonzero(mask)

        rand_vecs = random_unit_vector_batch(num_hits)

        scatter_directions = normals[mask] + rand_vecs

        is_zero = np.linalg.norm(scatter_directions, axis=-1) < 1e-8
        scatter_directions[is_zero] = normals[mask][is_zero]

        return scatter_directions, self.albedo

class Metal(Material):

    def __init__(self, albedo:np.ndarray, fuzz:float) -> None:
        self.albedo = albedo
        self.fuzz = fuzz
    
    def scatter_batch(self, rays_in, points, normals, front_faces, mask) -> tuple[np.ndarray, np.ndarray]:
        num_hits = np.count_nonzero(mask)

        v = rays_in.direction[mask]
        n = normals[mask]

        dot_product = np.sum(v * n, axis=-1, keepdims=True)
        reflected = v - 2 * dot_product * n

        if self.fuzz > 0:
            reflected  += self.fuzz  * random_unit_vector_batch(num_hits)
        
        return reflected, self.albedo

class Dielectric(Material):
    def __init__(self, refraction_index: float) -> None:
        self.refraction_index = refraction_index

    def scatter_batch(self, rays_in, points, normals, front_faces, mask):
        # Use front_faces to decide the refraction ratio
        ri = np.where(front_faces[mask], (1.0 / self.refraction_index), self.refraction_index)
        
        unit_dirs = rays_in.direction[mask] / np.linalg.norm(rays_in.direction[mask], axis=-1, keepdims=True)
        n = normals[mask]
        
        cos_theta = np.minimum(np.sum(-unit_dirs * n, axis=-1), 1.0)
        sin_theta = np.sqrt(np.maximum(0, 1.0 - cos_theta**2))

        # Reflect or Refract?
        cannot_refract = (ri * sin_theta) > 1.0
        reflectance = self.reflectance_batch(cos_theta, ri)
        num_hits = np.count_nonzero(mask)
        do_reflect = cannot_refract | (reflectance > np.random.uniform(0, 1, num_hits))
        
        # Reflection
        res_reflected = unit_dirs - 2 * np.sum(unit_dirs * n, axis=-1, keepdims=True) * n
        
        # Refraction
        perp = ri[..., np.newaxis] * (unit_dirs + cos_theta[..., np.newaxis] * n)
        parallel = -np.sqrt(np.abs(1.0 - np.sum(perp**2, axis=-1, keepdims=True))) * n
        res_refracted = perp + parallel
        
        # Choose path based on the mask
        final_dirs = np.where(do_reflect[..., np.newaxis], res_reflected, res_refracted)
        
        return final_dirs, np.array([1.0, 1.0, 1.0], dtype=np.float32)

    @staticmethod
    def reflectance_batch(cosine, ref_idx):
        r0 = ((1 - ref_idx) / (1 + ref_idx))**2
        return r0 + (1 - r0) * (1 - cosine)**5