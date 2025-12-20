from math import sqrt

from hittable import HitRecord, Hittable
from ray import Ray
from vec3 import Vec3, dot

Point3 = Vec3

class Sphere(Hittable):

    def __init__(self, center:Point3, radius:float) -> None:

        self.center = center
        self.radius = radius
    
    def hit(self, r: Ray, t_min: float, t_max: float) -> tuple[bool, HitRecord | None]:
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
        if (root <= t_min or root >= t_max):
            root = (h + sqrtd) / a
            if (root <= t_min or root >= t_max):
                return (False, None)
        
        record:HitRecord = HitRecord(root, r.at(root), (r.at(root) -  self.center)/ self.radius)

        return True, record

