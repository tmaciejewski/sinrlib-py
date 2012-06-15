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
            self.links[uid] = []

            for uid2, node2 in self.nodes.iteritems():
                if node - node2 <= (1 - range_e) * self.config.range:
                    self.links[uid].append(uid2)
                    self.links[uid2].append(uid)
        
            self.nodes[uid] = node
            uid += 1

            if len(self.nodes) >= n:
                if len(self.connected_components()) == 1:
                    return
