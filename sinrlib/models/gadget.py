import model, random, math

class GadgetModel(model.Model):
    def generate(self, m, p, e):
        self.nodes = {}
        self.links = {}
        
        s = (1 - e) * self.config.range / math.sqrt(2)
        source_x = 0
        source_y = 0
        uid = 0

        for _ in range(m):
            recent_nodes = []
            for _ in range(p)[1:]:
                x = source_x + s * random.random()
                y = source_y + s

                self.nodes[uid] = model.Node(x, y)
                self.links[uid] = []
                recent_nodes.append(uid)
                uid += 1

            new_source = random.choice(recent_nodes)
            source_x = self.nodes[new_source].x
            source_y = self.nodes[new_source].y + (1 - e) * self.config.range
            self.nodes[uid] = model.Node(source_x, source_y)
            self.links[uid] = []
            uid += 1
            

        for uid1, node1 in self.nodes.iteritems():
            for uid2, node2 in self.nodes.iteritems():
                if uid1 != uid2 and node1 - node2 <= self.config.range:
                    self.links[uid1].append(uid2)
