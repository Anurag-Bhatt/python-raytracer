from math import inf


class Interval:
    empty: "Interval"
    universe: "Interval"

    def __init__(self, min=inf, max=-inf) -> None:
        
        self.min:float = min
        self.max:float = max

    def size(self) -> float:
        return self.max - self.min
    
    def contains(self, x)-> bool:
        return self.min <= x and x <= self.max
    
    def surrounds(self, x) -> bool:
        return self.min < x and x < self.max
    
    def clamp(self, x:float) -> float:
        if x < self.min:
            return self.min
        if x > self.max:
            return self.max
        
        return x

Interval.empty = Interval(inf, -inf)
Interval.universe = Interval(-inf, inf)