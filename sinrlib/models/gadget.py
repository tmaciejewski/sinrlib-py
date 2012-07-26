import model, random, math

class GadgetModel(model.Model):
    def __init__(self, config, m, p, range_e):
        model.Model.__init__(self, config)

        self.nodes = {}
        self.links = {}
        
        s = range_e / math.sqrt(2)
        source_x = 0
        source_y = 0
        uid = 1

        self.nodes[0] = model.Node(source_x, source_y)
        self.links[0] = set()

        self.source = 0

        for _ in range(m):
            recent_nodes = []
            for _ in range(p)[1:]:
                x = source_x + s * random.random()
                y = source_y + s

                self.nodes[uid] = model.Node(x, y)
                self.links[uid] = set()
                recent_nodes.append(uid)
                uid += 1

            source = random.choice(recent_nodes)
            source_x = self.nodes[source].x
            source_y = self.nodes[source].y + range_e
            self.nodes[uid] = model.Node(source_x, source_y)
            self.links[uid] = {source}
            self.links[source].add(uid)
            uid += 1
            

        for uid1, node1 in self.nodes.iteritems():
            for uid2, node2 in self.nodes.iteritems():
                if uid1 != uid2 and node1 - node2 <= range_e:
                    if uid2 not in self.links[uid1]:
                        self.links[uid1].add(uid2)
