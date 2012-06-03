#!/usr/bin/python

import sys

sys.path.append('..')

import unittest
import config, noise.gev
from models import model

class ModelGEVTest(unittest.TestCase):
    def setUp(self):
        self.config = config.Config()
        self.config.power = -100
        self.config.noise = noise.gev.GEV(-90, 1.5)
        self.model = model.Model(self.config)
        self.nodes = {
                0 : model.Node(0, 0),
                1 : model.Node(1, 0),
                2 : model.Node(0, 0.1),
                3 : model.Node(1, 0.1),
                4 : model.Node(4, 0)
                }

        self.links = {
                0 : [1, 4],
                1 : [0],
                2 : [3],
                3 : [2],
                4 : [0]
                }

        self.model.nodes = self.nodes
        self.model.links = self.links
            
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
        self.nodes = {
                0 : model.Node(0, 0),
                1 : model.Node(1, 0),
                2 : model.Node(0, 0.1),
                3 : model.Node(1, 0.1),
                4 : model.Node(4, 0)
                }

        self.links = {
                0 : [1, 4],
                1 : [0],
                2 : [3],
                3 : [2],
                4 : [0]
                }

        self.model.nodes = self.nodes
        self.model.links = self.links
            
    def test_eval(self):
        l1 = (0, 1)
        l2 = (2, 3)
        l3 = (0, 4)
        [l1], [] = self.model.eval([l1])
        [l2], [] = self.model.eval([l2])
        [], [l1, l2] = self.model.eval([l1, l2])
        [], [l3] = self.model.eval([l3]) 

    def test_save_load(self):
        self.model.save('model.tmp')
        self.model.nodes = {}
        self.model.links = {}
        self.model.load('model.tmp')
        self.assertEqual(self.model.links, self.links)
        self.assertEqual(self.model.nodes, self.nodes)

class ConnectedComponentsTest(unittest.TestCase):
    def setUp(self):
        self.config = config.Config()
        self.model = model.Model(self.config)
        self.nodes = {
                0 : None,
                1 : None,
                2 : None,
                3 : None,
                4 : None,
                5 : None,
                }

        self.links = {
                0 : [1],
                1 : [0],
                2 : [3, 5],
                3 : [2, 4],
                4 : [3, 5],
                5 : [4, 2],
                }

        self.model.nodes = self.nodes
        self.model.links = self.links

    def connected_components_test(self):
        [C1, C2] = self.model.connected_components()
        self.assertIn(0, C1)
        self.assertIn(1, C1)
        self.assertIn(2, C2)
        self.assertIn(3, C2)
        self.assertIn(4, C2)
        self.assertIn(5, C2)

if __name__ == "__main__":
    unittest.main()
