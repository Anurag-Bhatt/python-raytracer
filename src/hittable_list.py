import numpy as np
from hittable import HitRecord, Hittable

from ray import Ray
from interval import Interval

class HittableList(Hittable):

    def __init__(self) -> None:
        self.objects = []

    def add(self, object:Hittable):
        self.objects.append(object)
    
    def clear(self):
        self.objects.clear()
    
    def hit(self, rays, t_min:float, t_max:float)-> tuple[np.ndarray, np.ndarray, np.ndarray]:
        
        image_shape = rays.origin.shape[:2]

        closest_t = np.full(image_shape, t_max, dtype=np.float32)
        hit_anything_mask = np.zeros(image_shape, dtype=bool)

        closet_obj_idx = np.full(image_shape, -1, dtype=np.int32)

        for idx, obj in enumerate(self.objects):

            hit_mask, t_values, obj_idx = obj.hit(rays, t_min, t_max)

            is_closer = hit_mask & (t_values < closest_t)

            closest_t[is_closer] = t_values[is_closer]
            closet_obj_idx[is_closer] = idx
            hit_anything_mask[is_closer] = True
        
        return hit_anything_mask, closest_t, closet_obj_idx
    
    def get_world_record(self, rays, hit_mask, t_values, obj_indices):

        final_points = np.zeros_like(rays.origin)
        final_normals = np.zeros_like(rays.origin)

        front_face = np.zeros(hit_mask.shape, dtype=bool)

        for idx, obj in enumerate(self.objects):
            relevant_mask =  hit_mask & (obj_indices == idx)

            if np.any(relevant_mask):

                p, n, ff = obj.get_record(rays, t_values, relevant_mask)

                final_points[relevant_mask] = p
                final_normals[relevant_mask] = n

                front_face[relevant_mask] = ff
        
        return final_points, final_normals, front_face