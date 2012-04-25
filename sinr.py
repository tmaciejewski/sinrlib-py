#!/usr/bin/python

import sinrlib.simulation, sinrlib.config
from sinrlib.noise.gev import GEV
import scipy

class Echo(sinrlib.simulation.Algorithm):
    def init(self, uid, links):
        if uid == 0:
            return links
        else:
            return []

    def compute(self, uid, msg, sender, links):
        return [sender]

class Broadcast(sinrlib.simulation.Algorithm):
    def init(self, uid, links):
        if uid == 0:
            return links
        else:
            return []

    def compute(self, uid, msg, sender, links):
        return [node for node in links if node != sender]

config1 = sinrlib.config.Config()
config1.noise = GEV(-90, 1.5, 0.25)
config1.power = -100
config1.beta = 1.1

model1 = sinrlib.model.Model(config1)
model1.add_node(0, 0, 0)
model1.add_node(1, 1, 0)
model1.link_nodes(0, 1)


config2 = sinrlib.config.Config()
config2.noise = GEV(5, 1.5, 0.25)
config2.power = 10000
config2.beta = 0.1

model2 = sinrlib.model.Model(config2)
model2.generate(10) 

simulation1 = sinrlib.simulation.Simulation(model1)
simulation1.run(10, Echo())

simulation2 = sinrlib.simulation.Simulation(model2)
simulation2.run(10, Broadcast())
