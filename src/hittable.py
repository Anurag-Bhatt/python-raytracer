from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from ray import Ray
from interval import Interval

if TYPE_CHECKING:
    from material import Material

@dataclass
class HitRecord:
    p:np.ndarray
    normal:np.ndarray
    t:float
    front_face:bool
    material : Material

    def set_face_normal(self, r:Ray, outward_normal:np.ndarray):
        
        self.front_face = np.dot(r.direction, outward_normal) < 0.0
        self.normal = outward_normal if self.front_face else -outward_normal

class Hittable(ABC):

    @abstractmethod
    def hit(self, r:Ray, ray_t:Interval) -> tuple[bool, HitRecord | None]:
        pass