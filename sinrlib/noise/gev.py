import math, random

class GEV:
    def __init__(self, mi, sigma, ksi = 0):
        self.mi = mi
        self.sigma = sigma
        self.ksi = ksi

    def __call__(self):
        x = 0
        while x == 0:
            x = random.random()

        if self.ksi == 0:
            return self.mi - self.sigma * math.log(-math.log(x))
        else:
            return self.mi - self.sigma * \
                (1 - (-math.log(x)) ** -self.ksi) / self.ksi
