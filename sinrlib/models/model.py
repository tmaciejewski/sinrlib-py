import math
import matplotlib.pyplot
import pickle

class Node:
    def __init__(self, x, y, noise = None):
        self.x = x
        self.y = y
        self.noise = noise

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
    def __sub__(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx**2 + dy**2)

    def __str__(self):
        return 'Node(%s, %s)' % (self.x, self.y)
        
    def __repr__(self):
        return self.__str__()

class Model:
    def __init__(self, config):
        self.config = config
        self.nodes = {}
        self.links = {}
        self.power_cache  = {}
        self.failed_transmit = 0
        self.success_transmit = 0

    def power(self, sender, receiver):
        try:
            return self.power_cache[(sender, receiver)]
        except KeyError:
            dist = self.nodes[sender] - self.nodes[receiver]
            p = self.config.power / dist ** self.config.alpha
            self.power_cache[(sender, receiver)] = p
            return self.power_cache[(sender, receiver)]

    def eval(self, senders):
        success = set()
        for sender in senders:
            for receiver in self.links[sender]:
                # nodes can't send and receive simultanously
                if receiver not in senders: 
                    interference = sum([self.power(node, receiver) \
                            for node in senders if node != sender])
                    noise = self.nodes[receiver].noise()
                    try:
                        SINR = self.power(sender, receiver) / (interference + noise)
                        if SINR >= self.config.beta:
                            success.add(receiver)
                            self.success_transmit += 1
                        else:
                            self.failed_transmit += 1
                    except ZeroDivisionError:
                        success.add(receiver)
                        self.success_transmit += 1
                
        return success

    def connected_components(self):
        components = []
        nodes = set(self.nodes.keys())

        while len(nodes) > 0:
            visited_nodes = set()
            queue = set([nodes.pop()])
            
            while len(queue) > 0:
                uid = queue.pop()
                visited_nodes.add(uid)
                queue.update(self.links[uid] - visited_nodes)

            components.append(visited_nodes)
            nodes -= visited_nodes

        return components
        
    def show(self, title = 'Network'):
        self.plot(title)
        matplotlib.pyplot.show()

    def plot(self, title):
        matplotlib.pyplot.cla()
        for s in self.links:
            for r in self.links[s]:
                if s < r:
                    xs = [self.nodes[s].x, self.nodes[r].x]
                    ys = [self.nodes[s].y, self.nodes[r].y]
                    matplotlib.pyplot.plot(xs, ys, 'b')

        xs = [v.x for v in self.nodes.values()]
        ys = [v.y for v in self.nodes.values()]
        matplotlib.pyplot.title(title)
        matplotlib.pyplot.plot(xs, ys, 'or', markersize = 8)

    def export_to_pdf(self, filename, title):
        self.plot(title)
        matplotlib.pyplot.savefig(filename)

    def save(self, filename):
        f = open(filename, 'wb')
        pickle.dump(self.nodes, f)
        pickle.dump(self.links, f)
        f.close()

    def load(self, filename):
        f = open(filename, 'rb')
        self.nodes = pickle.load(f)
        self.links = pickle.load(f)
