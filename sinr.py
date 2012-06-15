#!/usr/bin/python

import math, sys

from algorithms.naive import Algorithm1
from algorithms.density import DensityAlgorithm
from sinrlib.config import Config
from sinrlib.simulation import Simulation, AlgorithmFailed
from sinrlib.models.uniform import UniformModel
from sinrlib.noise.const import ConstNoise

def main():
    config = Config()
    model = UniformModel(config)
    tries = int(sys.argv[1])
    start, end, step = [int(arg) for arg in sys.argv[2].split(',')]

    for N in range(start, end + 1, step):
        results = []
        model.generate(100, 2, 0.5)
        for i in range(tries):
            e = 0.1
            #model.show()
            simulation = Simulation(model, lambda: ConstNoise(1.0))
            try:
                algorithm = DensityAlgorithm(config, e)
                results.append(simulation.run(algorithm))
            except AlgorithmFailed:
                for uid in algorithm.nodes:
                    if not uid in algorithm.active:
                        print model.nodes[uid], 'is inactive'
                sys.stdout.flush()
                model.show()


        avg = float(sum(results)) / tries
        std = math.sqrt(sum([(r - avg)**2 for r in results]) / tries)
        print N, avg, std
        sys.stdout.flush()

if __name__ == "__main__":
    #import cProfile
    #cProfile.run('main()')
    main()
