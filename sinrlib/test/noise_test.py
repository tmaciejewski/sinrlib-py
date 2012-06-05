#!/usr/bin/python

import sys

sys.path.append('..')

import unittest, noise.gev, noise.const, config

class GEVTest(unittest.TestCase):
    def setUp(self):
        self.config = config.Config()
        self.r1 = noise.gev.GEV(100, 1.5, 0.5)

    def test_next(self):
        v = self.r1()
        self.assertEqual(v, self.r1())
        self.assertEqual(v, self.r1())
        self.assertEqual(v, self.r1())
        self.r1.next()
        self.assertNotEqual(v, self.r1())

    def test_deterministicy(self):
        self.r1.reset()
        L1 = [self.r1.next() for _ in range(1000)]
        self.r1.reset()
        L2 = [self.r1.next() for _ in range(1000)]
        self.assertEqual(L1, L2)

    def test_range(self):
        c = self.config
        r = self.r1.range(c)
        prob = 1 - len([x for x in [(c.power / r**c.alpha) / self.r1.next() for _ in range(100000)] if x < c.beta]) / 100000.
        self.assertTrue(0.93 < prob < 0.96)        

class ConstNoiseTest(unittest.TestCase):
    def setUp(self):
        self.noise = noise.const.ConstNoise(4)
        self.config = config.Config()
        self.config.power = 196

    def test_value(self):
        self.assertEqual(self.noise(), 4)
        self.assertEqual(self.noise(), 4)
        self.noise.reset()
        self.assertEqual(self.noise(), 4)
        self.noise.next()
        self.assertEqual(self.noise(), 4)

    def test_range(self):
        self.assertEqual(7, self.noise.range(self.config))

if __name__ == "__main__":
    unittest.main()
