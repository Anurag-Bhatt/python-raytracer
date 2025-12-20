from abc import ABC, abstractmethod
from dataclasses import dataclass
from vec3 import Vec3
from ray import Ray

Point3 = Vec3

@dataclass
class HitRecord:
    p:Point3
    normal:Vec3
    t:float

class Hittable(ABC):

    @abstractmethod
    def hit(self, r:Ray, t_min:float, t_max:float) -> tuple[bool, HitRecord | None]:
        pass