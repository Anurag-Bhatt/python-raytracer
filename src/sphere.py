from __future__ import annotations
from interval import Interval

import numpy as np

from hittable import HitRecord, Hittable
from ray import Ray
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from material import Material


class Sphere(Hittable):

    def __init__(self, center:np.ndarray, radius:float, mat:Material) -> None:

        self.center = center
        self.radius = radius
        self.mat = mat
    
    def hit(self, r: Ray, ray_t:Interval) -> tuple[bool, HitRecord | None]:
        
        oc = self.center - r.origin 
        a = np.dot(r.direction, r.direction)
        h = np.dot(r.direction, oc)
        c = np.dot(oc, oc) - (self.radius**2)

        discriminant = h*h - (a*c)
        if discriminant < 0:
            return (False, None)
        
        sqrtd = np.sqrt(discriminant)

        # Finding the nearest root in the required range
        root = (h - sqrtd) / a
        if not (ray_t.surrounds(root)):
            root = (h + sqrtd) / a
            if not (ray_t.surrounds(root)):
                return (False, None)
        
        hit_point = r.at(root)
        outward_normal = (hit_point - self.center) / self.radius
        record:HitRecord = HitRecord(hit_point, outward_normal, root, False, self.mat)
        record.set_face_normal(r, outward_normal)

        return True, record