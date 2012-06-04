class ConstNoise:
    def __init__(self, n):
        self.n = n

    def reset(self):
        pass

    def range(self, config):
        return (config.power / (config.beta * self.n)) ** (1.0 / config.alpha)

    def __call__(self):
        return self.n
