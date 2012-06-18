#!/usr/bin/python

import math, sys

from matplotlib import pyplot

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

    C = 10
    e = 0.1
    S = 1

    avgs = []
    stds = []
    ns  = []

    for N in range(start, end + 1, step):
        results = []
        while len(results) < tries:
            try:
                model.generate(N, 1, 1 - 6*e)
                simulation = Simulation(model, lambda: ConstNoise(1.0))
                algorithm = DensityAlgorithm(config, e, C)
                results.append(simulation.run(algorithm))
                sys.stdout.write('.')
                sys.stdout.flush()
            except AlgorithmFailed:
                print 'algorithm failed!'
                for uid in algorithm.nodes:
                    if not uid in algorithm.active:
                        print model.nodes[uid], 'is inactive'
                #model.show()

        avg = float(sum(results)) / len(results)
        std = math.sqrt(sum([(r - avg)**2 for r in results]) / len(results))

        print
        print N, avg, std

        ns.append(N)
        avgs.append(avg)
        stds.append(std)

    pyplot.cla()
    pyplot.xlabel('Network size')
    pyplot.ylabel('Avg rounds number')
    pyplot.xlim(start - step, end + step)
    pyplot.title('Results with e = %f, S = %d, C = %f' % (e, S, C))
    pyplot.errorbar(ns, avgs, stds, ecolor = 'r')
    pyplot.show()

if __name__ == "__main__":
    #import cProfile
    #cProfile.run('main()')
    main()
