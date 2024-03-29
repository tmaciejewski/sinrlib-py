import random, math

class BackoffAlgorithm():
    def __init__(self, config):
        self.last_progress = 0

    def init(self, nodes, links, source):
        self.nodes = nodes
        self.N = len(nodes)
        self.active = set([source])
        self.phase = {}
        self.counter = {}
        self.density = {}
        for uid in self.nodes:
            self.phase[uid] = 1
            self.counter[uid] = 1
            neighbours = [u for u in self.nodes if u != uid \
                    and self.nodes[u] - self.nodes[uid] <= 1]
            self.density[uid] = len(neighbours)

    def on_round_end(self, uid, messages, round_number):
        if messages != []:
            self.active.add(uid)

        if uid in self.active:
            if self.counter[uid] > 0:
                self.counter[uid] -= 1
            if self.counter[uid] == 0:
                self.phase[uid] *= 2
                if self.phase[uid] > 2 * self.density[uid]:
                    self.counter[uid] = -1
                else:
                    self.counter[uid] = random.randint(1, self.phase[uid])
                return True
            else:
                return False

    def is_done(self):
        progress = len(self.active)
        if progress > self.last_progress:
            self.last_progress = progress
            #print 'progress:', float(progress) / self.N
        return len(self.active) == self.N

