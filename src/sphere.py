from __future__ import annotations
from math import sqrt
from interval import Interval

from hittable import HitRecord, Hittable
from ray import Ray
from vec3 import Vec3, dot
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from material import Material

Point3 = Vec3

class Sphere(Hittable):

    def __init__(self, center:Point3, radius:float, mat:Material) -> None:

        self.center = center
        self.radius = radius
        self.mat = mat
    
    def hit(self, r: Ray, ray_t:Interval) -> tuple[bool, HitRecord | None]:
        oc = self.center - r.origin 
        a = r.direction.length_squared()
        h = dot(r.direction, oc)
        c = oc.length_squared() - (self.radius * self.radius)

        discrimant = h*h - (a*c)
        if discrimant < 0:
            return (False, None)
        
        sqrtd = sqrt(discrimant)

        # Finding the nearest root in the required range
        root = (h - sqrtd) / a
        if not (ray_t.surrounds(root)):
            root = (h + sqrtd) / a
            if not (ray_t.surrounds(root)):
                return (False, None)
        
        record:HitRecord = HitRecord(r.at(root), (r.at(root) - self.center) / self.radius, root, False, self.mat)
        record.set_face_normal(r, (record.p - self.center) / self.radius)

        return True, record