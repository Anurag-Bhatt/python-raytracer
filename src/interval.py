from math import inf

class Interval:
    empty: "Interval"
    universe: "Interval"

    def __init__(self, min=inf, max=-inf) -> None:
        
        self.min = min
        self.max = max

    def size(self):
        return self.max - self.min
    
    def contains(self, x):
        return self.min <= x and x <= self.max
    
    def surrounds(self, x):
        return self.min < x and x < self.max

Interval.empty = Interval(inf, -inf)
Interval.universe = Interval(-inf, inf)