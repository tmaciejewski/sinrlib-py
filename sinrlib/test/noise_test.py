#!/usr/bin/python

import sys

sys.path.append('..')

import unittest, noise.gev

class GEVTest(unittest.TestCase):
    def test_deterministicy(self):
        self.r1 = noise.gev.GEV(100, 1.5)
        self.r2 = noise.gev.GEV(100, 1.5)

        for _ in range(1000):
            self.assertEqual(self.r1(), self.r2())

if __name__ == "__main__":
    unittest.main()
