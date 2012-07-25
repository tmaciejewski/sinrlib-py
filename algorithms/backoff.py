import random, math

class BackoffAlgorithm():
    def __init__(self, config):
        self.last_progress = 0

    def init(self, nodes, links):
        self.nodes = nodes
        self.N = len(nodes)
        source = random.choice(self.nodes.keys())
        self.active = {source}
        self.phase = {}
        self.counter = {}
        for uid in self.nodes:
            self.phase[uid] = 1
            self.counter[uid] = 1
        return {}

    def on_round_end(self, uid, messages, round_number):
        if messages != []:
            self.active.add(uid)

        if uid in self.active:
            if self.counter[uid] > 0:
                self.counter[uid] -= 1
            if self.counter[uid] == 0:
                self.phase[uid] *= 2
                if self.phase[uid] > self.N:
                    self.counter[uid] = -1
                else:
                    self.counter[uid] = random.randint(1, self.phase[uid])
                return True
            else:
                return False

    def is_done(self):
        return len(self.active) == self.N

