#!/usr/bin/python

import sys, random

sys.path.append('..')

from config import Config
from models.gauss import GaussModel
from models.uniform import UniformModel
from models.social import SocialModel
from models.gadget import GadgetModel

config = Config()
config.range = 1

#model = GaussModel(config)
#model.generate(50, .85)

#model = UniformModel(config)
#model.generate(200, 8)

#model = SocialModel(config)
#model.generate(10, 3, 1, 0.2)

model = GadgetModel(config)
model.generate(5, 15, 0.1)

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
