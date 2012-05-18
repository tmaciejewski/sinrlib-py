#!/usr/bin/python

import sys

sys.path.append('..')

import unittest, config, models
from models.gauss import GaussModel
from models.uniform import UniformModel

class ModelTest(unittest.TestCase):
    def setUp(self):
        self.config = config.Config()
        #self.model = GaussModel(self.config)
        #self.model.generate(50, .85)

        self.model = UniformModel(self.config)
        self.model.generate(100, 8)

    def test_show(self):
        self.model.show()            
 
if __name__ == "__main__":
    unittest.main()
