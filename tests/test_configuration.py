#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testing the `Configuration` module by passing various arguments
"""

import sys
sys.path.append('../klpt')
import unittest
from klpt.preprocess import Preprocess
from klpt.configuration import Configuration
import json
import klpt

class TestPreprocess(unittest.TestCase):
    """ Test unit for the Preprocess class"""
    def setUp(self):                    
        with open(klpt.get_data("data/default-options.json"), encoding = "utf-8") as f:
            self.options = json.load(f)

    def tearDown(self):
        pass

    def testInsufficientArgs(self):
        for dialect in self.options["dialects"]:
            for script in self.options["scripts"]:
                for numeral in self.options["numerals"]:
                    Configuration({"dialect": dialect, "script": script, "numeral": numeral})

if __name__ == '__main__':
    unittest.main()
    