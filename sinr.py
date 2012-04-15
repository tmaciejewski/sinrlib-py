#!/usr/bin/python

import sinrlib.model, sinrlib.config
import scipy

config = sinrlib.config.Config()
model  = sinrlib.model.Model(config)

links = [sinrlib.model.Link((0,0), (4,0))]

print model.eval(links)
