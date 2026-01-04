from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np

from hittable import HitRecord
from ray import Ray
from utility import cross, normalise, random_unit_vector, near_zero, reflect, refract

if TYPE_CHECKING:
    from hittable import HitRecord

class Material(ABC):

    @abstractmethod
    def scatter(self, ray_in:Ray, rec:HitRecord) -> tuple[bool, np.ndarray, Ray]:
        pass

class Lambertian(Material):

    def __init__(self, albedo:np.ndarray) -> None:
        self.albedo = albedo

    def scatter(self, ray_in: Ray, rec: HitRecord) -> tuple[bool, np.ndarray, Ray]:
        
        scatter_direction = rec.normal + random_unit_vector()

        if near_zero(scatter_direction):
            scatter_direction = rec.normal

        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        
        return (True, attenuation, scattered)

class Metal(Material):

    def __init__(self, albedo:np.ndarray, fuzz:float) -> None:
        self.albedo = albedo
        self.fuzz = fuzz
    
    def scatter(self, ray_in: Ray, rec: HitRecord) -> tuple[bool, np.ndarray, Ray]:
        
        reflected = reflect(ray_in.direction, rec.normal)
        reflected = normalise(reflected) + (self.fuzz * random_unit_vector())
        
        scattered = Ray(rec.p, reflected)
        attenuation = self.albedo
        did_scatter = np.dot(scattered.direction, rec.normal) > 0
        return (did_scatter, attenuation, scattered)

class Dielectric(Material):

    def __init__(self, refraction_index:float) -> None:
        self.refraction_index = refraction_index
    
    def scatter(self, ray_in: Ray, rec: HitRecord) -> tuple[bool, np.ndarray, Ray]:
        
        attenuation = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        ri = (1.0 / self.refraction_index) if rec.front_face else self.refraction_index

        unit_direction = normalise(ray_in.direction)

        cos_theta = min(np.dot(-unit_direction, rec.normal), 1.0)
        sin_theta = np.sqrt(1 - cos_theta * cos_theta)

        # According to Snell's law
        cannot_refract = ri * sin_theta > 1.0
        direction = np.array([0, 0, 0], dtype=np.float32)
        if cannot_refract:
            # MUST REFLECT
            direction = reflect(unit_direction, rec.normal)
        else:
            # CAN REFRACT
            direction = refract(unit_direction, rec.normal, ri)

        scattered = Ray(rec.p, direction)
        return (True, attenuation, scattered)
    
    # Using Schlick's approximation for reflectance
    @staticmethod
    def reflectance(cosine:float, refraction_index:float):
        r0 = (1 - refraction_index) / (1 + refraction_index)
        r0 = r0 * r0
        return r0 + (1 - r0)*pow((1-cosine), 5)