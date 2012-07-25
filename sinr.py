#!/usr/bin/python

import math, sys
import sinrlib, algorithms
from matplotlib import pyplot

def main():
    config = sinrlib.Config()
    tries = int(sys.argv[1])
    start, end, step = [int(arg) for arg in sys.argv[2].split(',')]

    C = 1
    e = 0.1
    S = 2
    d = 10
    config.range = 1 - 6*e

    avgs = []
    stds = []
    ns  = []

    for N in range(start, end + 1, step):
        for S in range(1, 7):
            results = []
            diams = []
            while len(results) < tries:
                try:
                    model = sinrlib.UniformModel(config, N, S)
                    #model = sinrlib.SocialModel(config, N, S, e, 0.1)
                    simulation = sinrlib.Simulation(model, lambda: sinrlib.ConstNoise(1.0))
                    #algorithm = algorithms.DensityUnknownAlgorithm(config, e, C)
                    #algorithm = algorithms.DensityKnownAlgorithm(config, e, C, d)
                    algorithm = algorithms.BackoffAlgorithm(config)
                    results.append(simulation.run(algorithm, 1000))
                    diams.append(model.diameter())
                    sys.stdout.write('.')
                    sys.stdout.flush()
                except sinrlib.AlgorithmFailed:
                    print >> sys.stderr, 'algorithm failed!'
                    print 'empty rounds:', simulation.empty_rounds
                    print 'failed:', model.failed_transmit
                    print 'success:', model.success_transmit
                    for uid in algorithm.nodes:
                        print >> sys.stderr, model.nodes[uid], 'ppb =', algorithm.ppb[uid]
                        if not uid in algorithm.active:
                            print >> sys.stderr, model.nodes[uid], 'is inactive'
                    model.show()

            avg = float(sum(results)) / len(results)
            std = math.sqrt(sum([(r - avg)**2 for r in results]) / len(results))
            avg_diam = float(sum(diams)) / len(diams)

            print
            print N, d, S, avg, std, avg_diam

            ns.append(N)
            avgs.append(avg)
            stds.append(std)


if __name__ == "__main__":
    import cProfile
    #cProfile.run('main()')
    main()
