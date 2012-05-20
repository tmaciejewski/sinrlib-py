import math
import matplotlib.pyplot
import pickle

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
    def __sub__(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx**2 + dy**2)

    def __str__(self):
        return 'Node(%s, %s)' % (self.x, self.y)
        

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

    def is_connected(self):
        visited_nodes = set()
        queue = [self.nodes.keys()[0]]
        
        while len(queue) > 0:
            uid = queue.pop()
            visited_nodes.add(uid)
            for neighbor in self.links[uid]:
                if not neighbor in visited_nodes:
                    queue.append(neighbor)

        return len(visited_nodes) == len(self.nodes)
        
    def show(self):
        for s in self.links:
            for r in self.links[s]:
                if s < r:
                    xs = [self.nodes[s].x, self.nodes[r].x]
                    ys = [self.nodes[s].y, self.nodes[r].y]
                    matplotlib.pyplot.plot(xs, ys, 'b')

        xs = [v.x for v in self.nodes.values()]
        ys = [v.y for v in self.nodes.values()]
        matplotlib.pyplot.plot(xs, ys, 'or', markersize = 8)
        matplotlib.pyplot.show()

    def save(self, filename):
        f = open(filename, 'wb')
        pickle.dump(self.nodes, f)
        pickle.dump(self.links, f)
        f.close()

    def load(self, filename):
        f = open(filename, 'rb')
        self.nodes = pickle.load(f)
        self.links = pickle.load(f)

