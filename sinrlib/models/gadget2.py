import model, random, math, uniform

class Gadget2Model(uniform.UniformModel):
    def __init__(self, config, N, S, e, range_mod):
        uniform.UniformModel.__init__(self, config, N, S, range_mod)
        uid = max(self.nodes.keys()) + 1

        x = 0
        y = -(range_mod + e)

        self.add_node(uid, x, y / 2.0, range_mod)
        uid += 1

        while x < S + range_mod + e:
            self.add_node(uid, x, y, range_mod)
            uid += 1
            x += range_mod - e

        while y < S + range_mod + e:
            self.add_node(uid, x, y, range_mod)
            uid += 1
            y += range_mod - e

        while x > -(range_mod + e):
            self.add_node(uid, x, y, range_mod)
            uid += 1
            x -= range_mod - e

        while y > -(range_mod + e):
            self.add_node(uid, x, y, range_mod)
            uid += 1
            y -= range_mod - e

    def add_node(self, uid, x, y, range_mod):
        node = model.Node(x, y)
        self.links[uid] = set()
        for uid2, node2 in self.nodes.iteritems():
            if node - node2 <= range_mod:
                self.links[uid].add(uid2)
                self.links[uid2].add(uid)

        self.nodes[uid] = node
