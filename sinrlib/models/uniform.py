import model, random

class UniformModel(model.Model):
    def generate(self, n, size, range_e):
        for _ in range(100):
            self.nodes = {}
            self.links = {}

            for uid in range(n):
                x = random.random() * size
                y = random.random() * size

                self.nodes[uid] = model.Node(x, y)
                self.links[uid] = []

            for uid1, node1 in self.nodes.iteritems():
                for uid2, node2 in self.nodes.iteritems():
                    if uid1 != uid2 and node1 - node2 <= (1 - range_e) * self.config.range:
                        self.links[uid1].append(uid2)
            
            if len(self.connected_components()) == 1:
                return
        
        raise Exception("Can't generate connected graph")
