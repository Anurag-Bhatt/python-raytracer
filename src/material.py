from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from math import sqrt

from hittable import HitRecord
from ray import Ray
from vec3 import Vec3, random_unit_vector, reflect, refract ,unit_vector, dot

if TYPE_CHECKING:
    from hittable import HitRecord

color = Vec3

class Material(ABC):

    @abstractmethod
    def scatter(self, ray_in:Ray, rec:HitRecord) -> tuple[bool, color, Ray]:
        pass

class Lambertian(Material):

    def __init__(self, albedo:color) -> None:
        self.albedo = albedo

    def scatter(self, ray_in: Ray, rec: HitRecord) -> tuple[bool, Vec3, Ray]:
        
        scatter_direction = rec.normal + random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        
        return (True, attenuation, scattered)

class Metal(Material):

    def __init__(self, albedo:color, fuzz:float) -> None:
        self.albedo = albedo
        self.fuzz = fuzz
    
    def scatter(self, ray_in: Ray, rec: HitRecord) -> tuple[bool, Vec3, Ray]:
        
        reflected = reflect(ray_in.direction, rec.normal)
        reflected = unit_vector(reflected) + (self.fuzz * random_unit_vector())
        
        scattered = Ray(rec.p, reflected)
        attenuation = self.albedo
        did_scatter = dot(scattered.direction, rec.normal) > 0
        return (did_scatter, attenuation, scattered)

class Dielectric(Material):

    def __init__(self, refraction_index) -> None:
        self.refraction_index = refraction_index
    
    def scatter(self, ray_in: Ray, rec: HitRecord) -> tuple[bool, Vec3, Ray]:
        
        attenuation = color(1.0, 1.0, 1.0)
        ri = (1.0 / self.refraction_index) if rec.front_face else self.refraction_index

        unit_direction:Vec3 = unit_vector(ray_in.direction)

        cos_theta = min(dot(-unit_direction, rec.normal), 1.0)
        sin_theta = sqrt(1 - cos_theta * cos_theta)

        # According to Snell's law
        cannot_refract = ri * sin_theta > 1.0
        direction:Vec3 = Vec3(0, 0, 0)
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