#!/usr/bin/python

import random, math
import sinrlib.simulation, sinrlib.config
from sinrlib.noise.gev import GEV
from sinrlib.noise.const import ConstNoise
from sinrlib.models.uniform import UniformModel

class Algorithm1(sinrlib.simulation.Algorithm):
    def init(self, nodes, links):
        self.nodes = nodes.keys()
        self.N = len(nodes)
        self.active = {}
        return {self.nodes[0]}

    def on_received(self, uid, message, sender):
        try:
            self.nodes.remove(uid)
            self.active[uid] = True
        except ValueError:
            pass
        return False

    def on_round_end(self, uid, round_number):
        try:
            if self.active[uid]:
                return random.random() < (2.0 / self.N)
        except KeyError:
            pass

        return False

    def is_done(self):
        return self.nodes == []

def main():
    config = sinrlib.config.Config()
    model = UniformModel(config, lambda: ConstNoise(1.0))
    tries = 1000
    results = []

    for i in range(tries):
        model.generate(10, 3)
        simulation = sinrlib.simulation.Simulation(model)
        results.append(simulation.run(Algorithm1()))

    avg = float(sum(results)) / tries

    print 'avg:', avg
    print 'std:', math.sqrt(sum([(r - avg)**2 for r in results]) / tries)

if __name__ == "__main__":
    main()
