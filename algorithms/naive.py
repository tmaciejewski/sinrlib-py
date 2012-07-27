import random

class NaiveAlgorithm():
    def init(self, nodes, links, source):
        self.nodes = nodes.keys()
        self.N = len(nodes)
        self.active = set([source])

    def on_round_end(self, uid, messages, round_number):
        if messages != []:
            self.active.add(uid)

        if uid in self.active:
            return random.random() < (2.0 / self.N)
        else:
            return False

    def is_done(self):
        return len(self.active) == self.N

