import scipy, scipy.linalg
import random

class Node:
    def __init__(self, x, y):
        self.pos = scipy.array((x, y))

class Model:
    def __init__(self, config):
        self.config = config
        self.nodes = []
        self.links = {}
    
    def generate(self, n):
        self.nodes = [Node(0, 0)]
        self.links[self.nodes[0]] = []

        while len(self.nodes) < n:
            parent = random.choice(self.nodes)
            x = int(random.gauss(parent.pos[0], 10))
            y = int(random.gauss(parent.pos[1], 10))
            child = Node(x, y)
            self.nodes.append(child)
            self.links[parent].append(child)
            self.links[child] = []

    def eval(self, links):
        interference = 0
        success = []
        failed = []

        for (s, r) in links:
            dist = scipy.linalg.norm(self.nodes[s].pos - self.nodes[r].pos)
            S = self.config.power / dist ** self.config.alpha
            interference += S
        
        for (s, r) in links:
            dist = scipy.linalg.norm(self.nodes[s].pos - self.nodes[r].pos)
            S = self.config.power / dist ** self.config.alpha
            local_interference = interference - S
            IN = local_interference + self.config.noise()

            if IN > 0:
                sinr = S / IN

                if sinr >= self.config.beta:
                    success.append((s, r))
                else:
                    failed.append((s, r))
            else:
                success.append((s, r))
                
        return success, failed
