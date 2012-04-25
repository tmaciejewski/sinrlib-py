#!/usr/bin/python

import sys

sys.path.append('..')

import unittest
import model, config, noise.gev

class ModelGEVTest(unittest.TestCase):
    def setUp(self):
        self.config = config.Config()
        self.config.power = -100
        self.config.noise = noise.gev.GEV(-90, 1.5)
        self.model = model.Model(self.config)
        self.model.add_node(0, 0)
        self.model.add_node(1, 0)
        self.model.add_node(0, 0.1)
        self.model.add_node(1, 0.1)
        self.model.add_node(4, 0)
            
    def test_eval(self):
        l1 = (0, 1)
        l2 = (2, 3)
        l3 = (0, 4)
        [l1], [] = self.model.eval([l1])
        [l2], [] = self.model.eval([l2])
        [], [l1, l2] = self.model.eval([l1, l2])
        [], [l3] = self.model.eval([l3]) 


class ModelTest(unittest.TestCase):
    def setUp(self):
        self.config = config.Config()
        self.model = model.Model(self.config)
        self.model.add_node(0, 0)
        self.model.add_node(1, 0)
        self.model.add_node(0, 0.1)
        self.model.add_node(1, 0.1)
        self.model.add_node(4, 0)

    def test_generate(self):
        m = model.Model(self.config)
        m.generate(10)
        for n in m.nodes:
            print 'node:', n.pos
            print 'links:', 
            for links in m.links[n]:
                print links.pos,
            print
            
    def test_eval(self):
        l1 = (0, 1)
        l2 = (2, 3)
        l3 = (0, 4)
        [l1], [] = self.model.eval([l1])
        [l2], [] = self.model.eval([l2])
        [], [l1, l2] = self.model.eval([l1, l2])
        [], [l3] = self.model.eval([l3]) 

if __name__ == "__main__":
    unittest.main()
