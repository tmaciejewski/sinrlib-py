import model, random

class UniformModel(model.Model):
    def __init__(self, config, n, size, range_mod):
        model.Model.__init__(self, config)

        self.nodes = {}
        self.links = {}
        uid = 0

        while True:
            x = random.random() * size
            y = random.random() * size

            node = model.Node(x, y)
            self.links[uid] = set([])

            for uid2, node2 in self.nodes.iteritems():
                if node - node2 <= range_mod:
                    self.links[uid].add(uid2)
                    self.links[uid2].add(uid)
        
            self.nodes[uid] = node
            uid += 1

            if len(self.nodes) >= n:
                for comp in self.connected_components():
                    if len(comp) >= n:
                        self.nodes = {uid : self.nodes[uid] for uid in comp}
                        self.links = {uid : self.links[uid].intersection(comp) for uid in comp}
                        self.source = random.choice(self.nodes.keys())
                        return
