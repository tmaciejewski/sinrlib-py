import math, random

class GEV:
    def __init__(self, mi, sigma, ksi = 0):
        self.rng = random.Random()
        self.init_state = self.rng.getstate()
        self.mi = mi
        self.sigma = sigma
        self.ksi = ksi
        self.reset()

    def reset(self):
        self.rng.setstate(self.init_state)
        self.next()

    def range(self, config):
        tmp = self.mi + (self.sigma * ((-math.log(.95))**(-self.ksi)) - 1) / self.ksi
        return (tmp * config.beta / config.power) ** (- 1.0 / config.alpha)

    def __call__(self):
        return self.value

    def next(self):
        self.value = self.random()
        return self.value

    def random(self):
        x = 0
        while x == 0:
            x = self.rng.random()

        if self.ksi == 0:
            return self.mi - self.sigma * math.log(-math.log(x))
        else:
            return self.mi - self.sigma * \
                (1 - (-math.log(x)) ** -self.ksi) / self.ksi
