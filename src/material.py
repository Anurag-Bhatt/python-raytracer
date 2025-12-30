from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from ray import Ray
from vec3 import Vec3, random_unit_vector, reflect

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

    def __init__(self, albedo:color) -> None:
        self.albedo = albedo
    
    def scatter(self, ray_in: Ray, rec: HitRecord) -> tuple[bool, Vec3, Ray]:
        
        reflected = reflect(ray_in.direction, rec.normal)
        scattered = Ray(rec.p, reflected)
        attenuation = self.albedo
        return (True, attenuation, scattered)
