#!/usr/bin/python

import sinrlib.simulation, sinrlib.config
from sinrlib.noise.gev import GEV
import scipy

def echo(uid, msg, sender, links):
    return sender

config = sinrlib.config.Config()
config.noise = GEV(-90, 1.5)
config.power = -100
config.beta = 1.1

model = sinrlib.model.Model(config)
model.nodes = [sinrlib.model.Node(0, 0), sinrlib.model.Node(1,0)]

simulation = sinrlib.simulation.Simulation(model)

links = [(0, 1)]

simulation.run(10, echo, links)
