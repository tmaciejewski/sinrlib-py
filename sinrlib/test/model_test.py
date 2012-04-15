#!/usr/bin/python

import sys

sys.path.append('..')

import unittest
import model, config

class LinkTest(unittest.TestCase):
    def setUp(self):
        pass

    def test(self):
        s = [1.0, 4.5]
        r = [0.0, 0.0]
        l1 = model.Link(s, r)
        (array_s, array_r) = l1
        s = array_s.tolist()
        r = array_r.tolist()

class ModelTest(unittest.TestCase):
    def setUp(self):
        self.config = config.Config()
        self.model  = model.Model(self.config)

    def test_single(self):
        l1 = model.Link([0,0], [1,0])
        l2 = model.Link([0,0.1], [1,0.1])
        l3 = model.Link([0,0], [4,0])
        [l1], [] = self.model.eval([l1])
        [l2], [] = self.model.eval([l2])
        [], [l1, l2] = self.model.eval([l1, l2])
        [], [l3] = self.model.eval([l3]) 

if __name__ == "__main__":
    unittest.main()
