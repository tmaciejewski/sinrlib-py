import model, random

class UniformModel(model.Model):
    def generate(self, n, size, range_e = 0):
        self.nodes = {}
        self.links = {}
        uid = 0

        while True:
            x = random.random() * size
            y = random.random() * size

            node = model.Node(x, y)
            self.links[uid] = set([])

            for uid2, node2 in self.nodes.iteritems():
                if node - node2 <= (1 - range_e) * self.config.range:
                    self.links[uid].add(uid2)
                    self.links[uid2].add(uid)
        
            self.nodes[uid] = node
            uid += 1

            if len(self.nodes) >= n:
                for comp in self.connected_components():
                    if len(comp) >= n:
                        self.nodes = {uid : self.nodes[uid] for uid in comp}
                        self.links = {uid : self.links[uid].intersection(comp) for uid in comp}
                        return
