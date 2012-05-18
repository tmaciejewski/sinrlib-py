import model, random

class GaussModel(model.Model):
    def generate(self, n, sigma):
        for _ in range(100):
            self.nodes = {}
            self.links = {}

            uid = 1

            self.nodes[0] = model.Node(0, 0)
            self.links[0] = []

            while len(self.nodes) < n:
                parent_uid = random.choice(self.nodes.keys())
                x = random.gauss(self.nodes[parent_uid].x, sigma)
                y = random.gauss(self.nodes[parent_uid].y, sigma)
                self.nodes[uid] = model.Node(x, y)
                self.links[uid] = []
                uid += 1

            for uid1, node1 in self.nodes.iteritems():
                for uid2, node2 in self.nodes.iteritems():
                    if uid1 != uid2 and node1 - node2 <= 1:
                        self.links[uid1].append(uid2)
                        self.links[uid2].append(uid1)

            
            if self.is_connected():
                return
        
        raise Exception("Can't generate a connected graph")
