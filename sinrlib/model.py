import scipy, scipy.linalg
import random

class Node:
    def __init__(self, x, y):
        self.pos = scipy.array((x, y))

class Model:
    def __init__(self, config):
        self.config = config
        self.nodes = {}
        self.links = {}

    def add_node(self, uid, x, y):
        if not uid in self.nodes:
            n = Node(x, y)
            self.nodes[uid] = n
            self.links[uid] = []
   
    def link_nodes(self, uid1, uid2):
        if not uid2 in self.links[uid1]:
            self.links[uid1].append(uid2)
        if not uid1 in self.links[uid2]:
            self.links[uid2].append(uid1)

    def generate(self, n):
        uid = 1
        self.add_node(0, 0, 0)
        while len(self.nodes) < n:
            parent_uid = random.choice(self.nodes.keys())
            x = int(random.gauss(self.nodes[parent_uid].pos[0], 10))
            y = int(random.gauss(self.nodes[parent_uid].pos[1], 10))
            self.add_node(uid, x, y)
            self.link_nodes(parent_uid, uid)
            uid += 1

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

            if IN != 0:
                sinr = S / IN

                if sinr >= self.config.beta:
                    success.append((s, r))
                else:
                    failed.append((s, r))
            else:
                success.append((s, r))
                
        return success, failed
