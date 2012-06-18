import random, math

class DensityAlgorithm():
    def __init__(self, config, e, C):
        self.alpha = config.alpha
        self.e = e
        self.C = C

    def eval_density(self, nodes, e):
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
                self.density[uid] = len(uids)
        

    def init(self, nodes, links):
        self.nodes = nodes.keys()
        self.N = len(nodes)
        self.density = {}
        self.active = set()
        self.d = self.C * self.e**3 * min(4, 1.0 / (self.alpha - 2), math.log(self.N))
        self.eval_density(nodes, self.e)


        return {random.choice(self.nodes)}

    def on_round_end(self, uid, messages, round_number):
        if messages == True:
                self.active.add(uid)

        if uid in self.active:
            #print 'd/D:', self.d,  self.density[uid]
            return random.random() < self.d / self.density[uid]
        else:
            return False

    def is_done(self):
        #print 'progress:', len(self.active) / float(self.N)
        return len(self.active) == self.N

if __name__ == "__main__":
    Algorithm1()

