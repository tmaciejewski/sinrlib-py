import model, random

class SocialModel(model.Model):
    def uniform_sel(self, s):
        x = s * random.random() 
        y = s * random.random() 

        return x, y

    def update_weights(self, s, e, uid):
        tiles = int(s / e) 
        node = self.nodes[uid]
        i = tiles - 1 - int(node.y / e)
        j = int(node.x / e)
        tile = i * tiles + j

        for uid1 in self.links[uid]:
            for uid2 in self.links[uid1]:
                if uid != uid2:
                    node2 = self.nodes[uid2]
                    i = tiles - 1 - int(node2.y / e)
                    j = int(node2.x / e)
                    tile2 = i * tiles + j

                    self.sec_links[tile].add(uid2)
                    self.sec_links[tile2].add(uid)

    def social_sel(self, s, e):
        tiles = int(s / e) 
        weights = [ len(links) for links in self.sec_links ]

        #print 'Weights: '
        #for i in range(tiles):
        #    for j in range(tiles):
        #        print weights[i * tiles + j], '   ',
        #    print

        tile = self.weight_random(weights)
        i = tile / tiles
        j = tile % tiles

        e_x, e_y = self.uniform_sel(e)
        x = j * e + e_x
        y = (tiles - i - 1) * e + e_y

        return x, y
        

    def weight_random(self, weights):
        weights_sum = sum(weights)
        
        if weights_sum == 0:
            return random.randint(0, len(weights) - 1)


        weight_level = weights[0] 
        i = 0
        r = random.random() * weights_sum
        while r > weight_level:
           i += 1
           weight_level += weights[i]

        return i

    def generate(self, n, s, e, gamma):
        self.nodes = {}
        self.links = {}
        uid = 0
        tiles = int(s / e) 

        self.sec_links = []
        for _ in range(tiles):
            for _ in range(tiles):
                self.sec_links.append(set())

        while True:
            if random.random() < gamma:
                # uniform
                #print 'Uniform selection'
                x, y = self.uniform_sel(s)
            else:
                # social
                #print 'Social selection'
                x, y = self.social_sel(s, e)
                
            node = model.Node(x, y)
            self.links[uid] = []

            for uid2, node2 in self.nodes.iteritems():
                if node - node2 <= self.config.range:
                    self.links[uid].append(uid2)
                    self.links[uid2].append(uid)

            self.nodes[uid] = node

            self.update_weights(s, e, uid)

            uid += 1

            components = self.connected_components()
            for comp in components:
                if len(comp) == n:
                    nodes = {}
                    links = {}
                    for uid in comp:
                        nodes[uid] = self.nodes[uid]
                        links[uid] = []
                        for uid2 in self.links[uid]:
                            if uid2 in comp:
                                links[uid].append(uid2)
                    self.nodes = nodes
                    self.links = links
                    return
