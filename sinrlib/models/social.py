import model, random

class SocialModel(model.Model):
    def uniform_sel(self, s):
        x = s * random.random() 
        y = s * random.random() 

        return x, y

    def eval_weights(self, e, tiles):
        sec_links = []

        for _ in range(tiles):
            for _ in range(tiles):
                sec_links.append(set())

        for uid, node in self.nodes.iteritems():
            i = tiles - 1 - int(node.y / e)
            j = int(node.x / e)
            tile = i * tiles + j
            for neighbor in self.links[uid]:
                for neighbor2 in self.links[neighbor]:
                    if uid != neighbor2:
                        sec_links[tile].add(neighbor2)

        return [len(links) for links in sec_links]

    def social_sel(self, s, e):
        tiles = int(s / e) 

        weights = self.eval_weights(e, tiles)

        #print 'Weights: '
        #for i in range(tiles):
        #    for j in range(tiles):
        #        print weights[i * tiles + j], '   ',
        #    print

        tile = self.weight_random(weights)
        i = tile / tiles
        j = tile % tiles

        #print 'Selected tile: %d (%d, %d)' % (tile, i, j)

        e_x, e_y = self.uniform_sel(e)
        x = j * e + e_x
        y = (tiles - i - 1) * e + e_y

        #print 'Returned: ', x, y

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
        for _ in range(100):
            self.nodes = {}
            self.links = {}

            for uid in range(n):
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

            #if self.is_connected():
            return
        
        raise Exception("Can't generate a connected graph")
