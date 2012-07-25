#!/usr/bin/python

import math, sys
import sinrlib, algorithms
from matplotlib import pyplot

def main():
    if len(sys.argv) < 3:
        print 'Usage: sinr.py tries N_start,N_end,N_step S_start,S_end,S_step'
        return

    config = sinrlib.Config()
    tries = int(sys.argv[1])
    N_start, N_end, N_step = [int(arg) for arg in sys.argv[2].split(',')]
    S_start, S_end, S_step = [float(arg) for arg in sys.argv[3].split(',')]

    C = 1
    e = 0.1
    S = 5
    d = 5
    config.range = 1

    avgs = []
    stds = []
    ns  = []

    alg = [ #algorithms.DensityUnknownAlgorithm(config, e, C), \
            algorithms.DensityKnownAlgorithm(config, e, C, d), \
            algorithms.BackoffAlgorithm(config), \
            ]

    for N in range(N_start, N_end + 1, N_step):
        S = S_start
        while S <= S_end:
            for algorithm in alg:
                results = []
                diams = []
                while len(results) < tries:
                    try:
                        model = sinrlib.UniformModel(config, N, S, 0.9)
                        #model = sinrlib.SocialModel(config, N, S, e, 0.1)
                        simulation = sinrlib.Simulation(model, lambda: sinrlib.ConstNoise(1.0))
                        results.append(simulation.run(algorithm, 100000))
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
                print algorithm.__class__.__name__, N, d, e, S, avg, std, avg_diam

                ns.append(N)
                avgs.append(avg)
                stds.append(std)

            S += S_step

if __name__ == "__main__":
    import cProfile
    #cProfile.run('main()')
    main()
