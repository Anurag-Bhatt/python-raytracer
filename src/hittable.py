from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np

from ray import Ray
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

@dataclass
class BatchHitRecord:
    p:np.ndarray
    normal:np.ndarray
    t:np.ndarray
    front_face:np.ndarray
    material : Material

class Hittable(ABC):

    @abstractmethod
    def hit(self, rays, t_min:float, t_max:float)-> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Returns:
            tuple[np.ndarray, np.ndarray] 
            (hit_mask: bool array, t_values: float array)
        """
        pass
