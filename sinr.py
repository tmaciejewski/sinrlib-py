#!/usr/bin/python

import math

from algorithms.naive import Algorithm1
from sinrlib.config import Config
from sinrlib.simulation import Simulation
from sinrlib.models.uniform import UniformModel
from sinrlib.noise.const import ConstNoise

def main():
    config = Config()
    model = UniformModel(config)
    tries = 1000
    results = []

    for i in range(tries):
        model.generate(10, 3)
        simulation = Simulation(model, lambda: ConstNoise(1.0))
        results.append(simulation.run(Algorithm1()))

    avg = float(sum(results)) / tries

    print 'avg:', avg
    print 'std:', math.sqrt(sum([(r - avg)**2 for r in results]) / tries)

if __name__ == "__main__":
    main()
