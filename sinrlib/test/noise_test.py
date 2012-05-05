#!/usr/bin/python

import sys

sys.path.append('..')

import unittest, noise.gev

class GEVTest(unittest.TestCase):
    def test_deterministicy(self):
        self.r1 = noise.gev.GEV(100, 1.5)

        L1 = [self.r1() for _ in range(1000)]
        self.r1.reset()
        L2 = [self.r1() for _ in range(1000)]
        self.assertEqual(L1, L2)

if __name__ == "__main__":
    unittest.main()
