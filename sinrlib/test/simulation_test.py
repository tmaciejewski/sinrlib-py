#!/usr/bin/python

import sys

sys.path.append('..')

import unittest
from models import model
from noise import const
import simulation, config

class SimulationTest(unittest.TestCase):
    def setUp(self):
        self.config = config.Config()
        self.model = model.Model(self.config)
        self.nodes = {
                0 : model.Node(0, 0, const.ConstNoise(1)),
                1 : model.Node(1, 0, const.ConstNoise(1)),
                2 : model.Node(2, 0, const.ConstNoise(1)),
                }

        self.links = {
                0 : [1],
                1 : [0, 2],
                3 : [1],
                }

        self.model.nodes = self.nodes
        self.model.links = self.links

        self.simulation = simulation.Simulation(self.model)

        class TestAlgorithm1(simulation.Algorithm):
            def init(self, nodes, links):
                self.nodes = nodes.keys()
                return set([0])

            def on_received(self, uid, message, sender):
                self.nodes.remove(uid)
                return True

            def is_done(self):
                return self.nodes == []

        class TestAlgorithm2(simulation.Algorithm):
            def init(self, nodes, links):
                return set()

            def on_received(self, uid, message, sender):
                return True

            def is_done(self):
                return False

        self.algorithm1 = TestAlgorithm1()
        self.algorithm2 = TestAlgorithm2()

    def test_correct_simulation(self):
        self.assertEqual(2, self.simulation.run(self.algorithm1))

    def test_failed_simulation(self):
        self.assertEqual(-1, self.simulation.run(self.algorithm2))

if __name__ == "__main__":
    unittest.main()
