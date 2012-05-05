#!/usr/bin/python

import sys

sys.path.append('..')

import unittest
import model, config

class ModelTest(unittest.TestCase):
    def setUp(self):
        self.config = config.Config()
        self.model = model.Model(self.config)
        self.model.generate(40)

    def test_show(self):
        self.model.show()            
 
if __name__ == "__main__":
    unittest.main()
