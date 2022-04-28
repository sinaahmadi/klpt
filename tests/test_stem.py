#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../klpt')
import unittest
from klpt.stem import Stem
import json
import klpt

class TestStem(unittest.TestCase):
    """ Test unit for the Stem class"""
    def setUp(self):
        with open(klpt.get_data("data/test_cases_stem.json"), encoding = "utf-8") as f:
            self.test_cases = json.load(f)
                    
        with open(klpt.get_data("data/default-options.json"), encoding = "utf-8") as f:
            self.options = json.load(f)

    def tearDown(self):
        pass

    def test_analyze(self):
        for dialect in self.options["dialects"]:
            for script in self.options["scripts"]:
                if (dialect == "Sorani" and script == "Arabic") or (dialect == "Kurmanji" and script == "Latin"): 
                    stemmer = Stem(dialect, script)
                    # test the morphological analyzer
                    for test_case in self.test_cases["analyze"][dialect][script]:
                        self.assertCountEqual(stemmer.analyze(test_case), self.test_cases["analyze"][dialect][script][test_case])

                    # test the stemmer
                    # print(dialect, script)
                    for test_case in self.test_cases["stem"][dialect][script]:
                        for case in test_case["cases"]:
                            self.assertCountEqual(stemmer.stem(case, mark_unknown=test_case["parameters"]["mark_unknown"]), test_case["cases"][case])
                    
                    # test the lemmatizer
                    for test_case in self.test_cases["lemmatize"][dialect][script]:
                        # order of the lemmata may cause an error. Run many times.
                        self.assertCountEqual(stemmer.lemmatize(test_case), self.test_cases["lemmatize"][dialect][script][test_case])

                else: # otherwise, not supported currently
                    pass

if __name__ == "__main__":
    unittest.main()
