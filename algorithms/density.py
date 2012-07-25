import random, math

class DensityAlgorithm():
    def __init__(self, config, e, C):
        self.alpha = config.alpha
        self.e = e
        self.C = C

    def eval_ppb(self, nodes, e):
        density = {}
        for uid in nodes:
            x = int(nodes[uid].x / e)
            y = int(nodes[uid].y / e)
            if (x, y) in density:
                density[(x,y)].append(uid)
            else:
                density[(x, y)] = [uid]

        for uids in density.itervalues():
            for uid in uids:
                self.ppb[uid] = self.d / len(uids)
                #print uid, 'ppb:', self.d, '/',  len(uids), '=', self.ppb[uid]

    def init(self, nodes, links):
        self.nodes = nodes.keys()
        self.N = len(nodes)
        self.ppb = {}
        self.d = self.C * self.e**3 * min(4, 1.0 / (self.alpha - 2), math.log(self.N))
        self.eval_ppb(nodes, self.e)
        source = random.choice(self.nodes)
        self.active = {source}
        return self.active

    def on_round_end(self, uid, messages, round_number):
        if messages != []:
                self.active.add(uid)

        if uid in self.active:
            return random.random() < self.ppb[uid]
        else:
            return False

    def is_done(self):
        #print 'progress:', len(self.active) / float(self.N)
        return len(self.active) == self.N
