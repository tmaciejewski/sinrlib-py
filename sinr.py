#!/usr/bin/python

import math, sys
import sinrlib, algorithms

def main():
    if len(sys.argv) < 3:
        print 'Usage: sinr.py tries N_start,N_end,N_step S_start,S_end,S_step'
        return

    config = sinrlib.Config()
    tries = int(sys.argv[1])
    N_start, N_end, N_step = [int(arg) for arg in sys.argv[2].split(',')]
    S_start, S_end, S_step = [float(arg) for arg in sys.argv[3].split(',')]

    C = 1
    e = 0.2
    d = 10

    alg = [ #algorithms.DensityUnknownAlgorithm(config, e, C, d, d), \
            algorithms.DensityKnownAlgorithm(config, e, C, d), \
            #algorithms.BackoffAlgorithm(config), \
            algorithms.BackoffAckAlgorithm(config), \
            ]

    for N in range(N_start, N_end + 1, N_step):
        S = S_start
        while S <= S_end:
            results = {}
            diams = []
            for algorithm in alg:
                results[algorithm] = []
            for _ in range(tries):
                model = sinrlib.UniformModel(config, N, S, 1 - e)
                #model = sinrlib.SocialModel(config, N, S, e, 0.1, 1 - e)
                #model = sinrlib.GadgetModel(config, 15, 50, 1 - e)
                #model = sinrlib.Gadget2Model(config, N, S, e, 1 - e)
                #model.show()

                diameter = model.diameter()
                diams.append(diameter)
                for algorithm in alg:
                    try:
                        simulation = sinrlib.Simulation(model, lambda: sinrlib.ConstNoise(1.0))
                        r = simulation.run(algorithm, 100000)
                        results[algorithm].append(r)
                        sys.stdout.write('.')
                        sys.stdout.flush()
                    except sinrlib.AlgorithmFailed:
                        print >> sys.stderr, 'algorithm', algorithm, 'failed for N = %s, S = %s' % (N, S)
                        #model.show()
                sys.stdout.write(',')
                sys.stdout.flush()
            print 


            for algorithm in results:
                res = results[algorithm]
                avg = float(sum(res)) / len(res)
                std = math.sqrt(sum([(r - avg)**2 for r in res]) / len(res))
                avg_diam = float(sum(diams)) / len(diams)
    
                print algorithm.__class__.__name__, N, d, e, S, avg, std, avg_diam, avg / avg_diam

            S += S_step

if __name__ == "__main__":
    import cProfile
    #cProfile.run('main()')
    main()
