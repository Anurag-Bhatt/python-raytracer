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
    
    def hit(self, r: Ray, ray_t:Interval) -> tuple[bool, HitRecord | None]:
        
        final_rec = None
        hit_anything:bool = False
        closest_so_far:float = ray_t.max

        for obj in self.objects:
            hit, temp_rec = obj.hit(r, ray_t.min, closest_so_far)
            if hit:
                hit_anything = True
                closest_so_far = temp_rec.t
                final_rec = temp_rec
        
        return hit_anything, final_rec
                


