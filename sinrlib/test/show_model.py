#!/usr/bin/python

import sys

sys.path.append('..')

import unittest
import models.gauss, config

class ModelTest(unittest.TestCase):
    def setUp(self):
        self.config = config.Config()
        self.model = models.gauss.GaussModel(self.config)
        self.model.generate(50, .5)

    def test_show(self):
        self.model.show()            
 
if __name__ == "__main__":
    unittest.main()
