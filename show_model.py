#!/usr/bin/python

import sys, random
import sinrlib

def main():
    N = 200
    s = 5
    e = .2

    config = sinrlib.Config()

    if sys.argv[1] == 'uniform':
        model = sinrlib.UniformModel(config, N, s, 1-e)
    elif sys.argv[1] == 'social':
        model = sinrlib.SocialModel(config, N, s, e, .1, 1 - e)
        
        #print 'Weights: '
        #for i in range(model.tiles):
        #    for j in range(model.tiles):
        #        print len(model.sec_links[i * model.tiles + j]), '\t',
        #    print

        #print 'Should be: '
        #for i in range(model.tiles):
        #    for j in range(model.tiles):
        #        tile = i * model.tiles + j
        #        sec_links = set()
        #        for uid in model.nodes:
        #            uid_i = model.tiles - 1 - int(model.nodes[uid].y / e)
        #            uid_j = int(model.nodes[uid].x / e)
        #            if tile == uid_i * model.tiles + uid_j:
        #0                for uid1 in model.links[uid]:
        #                    for uid2 in model.links[uid1]:
        #                        if uid != uid2:
        #                            sec_links.add(uid2)
        #        print len(sec_links), '\t',
        #    print

    elif sys.argv[1] == 'gadget':
        model = sinrlib.GadgetModel(config, 10, 5, 0.1)

    print 'generated'

    #for i in range(100):
    #    n = random.randint(30,200)
    #    s = 5
    #    title = 'Uniform %d, n = %d, s = %d' % (i, n, s)
    #    try:
    #        model.generate(n, s)
    #        model.export_to_pdf('uniform%d.png' % i, title)
    #    except:
    #        pass                

    model.show(title = 'Network')            
    #model.export_to_pdf('model.png', 'N = %d' % N)

if __name__ == "__main__":
    import cProfile
    #cProfile.run('main()')
    main()
