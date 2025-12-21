from abc import ABC, abstractmethod
from dataclasses import dataclass
from vec3 import Vec3, dot
from ray import Ray
from interval import Interval

Point3 = Vec3

@dataclass
class HitRecord:
    p:Point3
    normal:Vec3
    t:float
    front_face:bool

    def set_face_normal(self, r:Ray, outward_normal:Vec3):
        
        self.front_face = dot(r.direction, outward_normal) < 0.0
        self.normal = outward_normal if self.front_face else -outward_normal

class Hittable(ABC):

    @abstractmethod
    def hit(self, r:Ray, ray_t:Interval) -> tuple[bool, HitRecord | None]:
        pass