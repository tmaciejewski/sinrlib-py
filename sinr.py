#!/usr/bin/python

import sinr_config
import sinr_model

import scipy

config = sinr_config.SINRConfig()
model  = sinr_model.SINRModel(config)

links = [(scipy.array([0,0]), scipy.array([4,0]))]

print model.eval(links)
