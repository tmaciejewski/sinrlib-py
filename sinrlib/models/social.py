import model, random, math

class SocialModel(model.Model):
    def uniform_sel(self, s):
        x = s * random.random() 
        y = s * random.random() 

        return x, y

    def update_weights(self, uid):
        tile = self.uid_to_tile[uid]
        tiles2 = set()
        uid_sec_links = set()
        for uid1 in self.links[uid]:
            tile1 = self.uid_to_tile[uid1]
            
            # tell my link about my other links
            self.sec_links[tile1].update(self.links[uid].difference(set([uid1])))
            
            for uid2 in self.links[uid1]:
                if uid != uid2:
                    tiles2.add(self.uid_to_tile[uid2])
                    self.sec_links[tile].add(uid2)

        for tile2 in tiles2:
            self.sec_links[tile2].add(uid)

    def social_sel(self, e):
        weights = [ len(links) for links in self.sec_links ]

        tile = self.weight_random(weights)
        i = tile / self.tiles
        j = tile % self.tiles

        e_x, e_y = self.uniform_sel(e)
        x = j * e + e_x
        y = (self.tiles - i - 1) * e + e_y

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

    def __init__(self, config, n, s, e, gamma, range_e):
        model.Model.__init__(self, config)

        self.nodes = {}
        self.links = {}
        self.uid_to_tile = {}
        self.tiles = int(math.ceil(float(s) / e)) 
        uid = 0

        self.sec_links = []
        for _ in range(self.tiles):
            for _ in range(self.tiles):
                self.sec_links.append(set())

        while True:
            if random.random() < gamma:
                # uniform
                x, y = self.uniform_sel(s)
            else:
                # social
                x, y = self.social_sel(e)
                
            node = model.Node(x, y)
            self.links[uid] = set()

            i = self.tiles - 1 - int(y / e)
            j = int(x / e)
            self.uid_to_tile[uid] = i * self.tiles + j

            for uid2, node2 in self.nodes.iteritems():
                if node - node2 <= range_e:
                    self.links[uid].add(uid2)
                    self.links[uid2].add(uid)

            self.nodes[uid] = node

            self.update_weights(uid)

            uid += 1

            #if len(self.nodes) % 100 == 0:
            #    print 'len:', len(self.nodes)

            if len(self.nodes) >= n:
                for comp in self.connected_components():
                    if len(comp) >= n:
                        self.nodes = {uid : self.nodes[uid] for uid in comp}
                        self.links = {uid : self.links[uid].intersection(comp) for uid in comp}
                        self.source = random.choice(self.nodes.keys())
                        return
