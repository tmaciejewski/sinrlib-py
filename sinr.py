#!/usr/bin/python

import math

from algorithms.naive import Algorithm1
from algorithms.density import DensityAlgorithm
from sinrlib.config import Config
from sinrlib.simulation import Simulation
from sinrlib.models.uniform import UniformModel
from sinrlib.noise.const import ConstNoise

def main():
    config = Config()
    model = UniformModel(config)
    tries = 1
    results = []

    for i in range(tries):
        e = 0.2
        model.generate(100, 1, 0.8)
        #model.show()
        simulation = Simulation(model, lambda: ConstNoise(1.0))
        results.append(simulation.run(DensityAlgorithm(config, e)))

    avg = float(sum(results)) / tries

    print 'avg:', avg
    print 'std:', math.sqrt(sum([(r - avg)**2 for r in results]) / tries)

if __name__ == "__main__":
    main()
