#!/usr/bin/python

import sys, random

sys.path.append('sinrlib')

from config import Config
from models.gauss import GaussModel
from models.uniform import UniformModel
from models.social import SocialModel
from models.gadget import GadgetModel

def main():
    config = Config()

    if sys.argv[1] == 'uniform':
        model = UniformModel(config)
        model.generate(200, 8)
    elif sys.argv[1] == 'social':
        model = SocialModel(config)
        model.generate(200, 10, 2, 0.1)
    elif sys.argv[1] == 'gadget':
        model = GadgetModel(config)
        model.generate(10, 5, 0.1)

    #for i in range(100):
    #    n = random.randint(30,200)
    #    s = 5
    #    title = 'Uniform %d, n = %d, s = %d' % (i, n, s)
    #    try:
    #        model.generate(n, s)
    #        model.export_to_pdf('uniform%d.png' % i, title)
    #    except:
    #        pass                

    model.show('Network')            

if __name__ == "__main__":
    main()
