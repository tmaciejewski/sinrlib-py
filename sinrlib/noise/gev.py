import math, random

class GEV:
    def __init__(self, mi, sigma):
        self.mi = mi
        self.sigma = sigma

    def __call__(self):
        x = random.random()
        while x == 0:
            x = random.random()

        return self.mi - self.sigma * math.log(-math.log(x))
