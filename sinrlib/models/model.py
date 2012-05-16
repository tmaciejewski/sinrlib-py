import math
import matplotlib.pyplot

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __sub__(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx**2 + dy**2)
        

class Model:
    def __init__(self, config):
        self.config = config
        self.nodes = {}
        self.links = {}

    def eval(self, links):
        interference = 0
        success = []
        failed = []

        for (s, r) in links:
            dist = self.nodes[s] - self.nodes[r]
            S = self.config.power / dist ** self.config.alpha
            interference += S
        
        for (s, r) in links:
            dist = self.nodes[s] - self.nodes[r]
            S = self.config.power / dist ** self.config.alpha
            local_interference = interference - S
            IN = local_interference + self.config.noise()

            if IN != 0:
                sinr = S / IN

                if sinr >= self.config.beta:
                    success.append((s, r))
                else:
                    failed.append((s, r))
            else:
                success.append((s, r))
                
        return success, failed
        
    def show(self):
        xs = [v.x for v in self.nodes.values()]
        ys = [v.y for v in self.nodes.values()]

        matplotlib.pyplot.plot(xs, ys, 'or')

        for s in self.links:
            for r in self.links[s]:
                xs = [self.nodes[s].x, self.nodes[r].x]
                ys = [self.nodes[s].y, self.nodes[r].y]
                matplotlib.pyplot.plot(xs, ys, 'b')

        matplotlib.pyplot.show()
