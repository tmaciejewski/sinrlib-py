import random, math

class DensityKnownAlgorithm():
    def __init__(self, config, e, C, d):
        self.alpha = config.alpha
        self.e = e
        self.C = C
        self.d = d
        self.last_progress = 0
        self.phase_round = 0

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
                self.ppb[uid] = float(self.C) / len(uids)
                #print uid, 'ppnb = ', self.ppb[uid]

    def init(self, nodes, links):
        self.nodes = nodes
        self.N = len(nodes)
        gamma = self.e / (2 * math.sqrt(2))
        self.ppb = {}
        self.eval_ppb(nodes, self.e)
        self.box = {}
        for uid in nodes:
            box_x = int(nodes[uid].x / gamma)
            box_y = int(nodes[uid].y / gamma)
            self.box[uid] = (box_x, box_y)

        source = random.choice(self.nodes.keys())
        self.active = {source}
        return {}

    def on_round_end(self, uid, messages, round_number):
        if messages != []:
                self.active.add(uid)

        if uid in self.active:
            a = int(self.phase_round / self.d)
            b = int(self.phase_round % self.d)
            if self.box[uid][0] % self.d == a and self.box[uid][1] % self.d == b:
                return random.random() < self.ppb[uid]
            else:
                return False
        else:
            return False

    def is_done(self):
        self.phase_round += 1
        if self.phase_round == self.d**2:
            self.phase_round = 0

        progress = len(self.active) / float(self.N)
        if progress > self.last_progress:
            self.last_progress = progress
            #print 'progress:', progress
        return len(self.active) == self.N

if __name__ == "__main__":
    Algorithm1()
