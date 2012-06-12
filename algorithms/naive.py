import random

class Algorithm1():
    def init(self, nodes, links):
        self.nodes = nodes.keys()
        self.N = len(nodes)
        self.active = {}
        return {self.nodes[0]}

    def on_round_end(self, uid, messages, round_number):
        if messages == True:
            try:
                self.nodes.remove(uid)
                self.active[uid] = True
            except ValueError:
                pass

        try:
            if self.active[uid]:
                return random.random() < (2.0 / self.N)
        except KeyError:
            pass

        return False

    def is_done(self):
        return self.nodes == []

if __name__ == "__main__":
    Algorithm1()

