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
        with open(klpt.get_data("data/test_cases_stem.json")) as f:
            self.test_cases = json.load(f)
                    
        with open(klpt.get_data("data/default-options.json")) as f:
            self.options = json.load(f)

    def tearDown(self):
        pass

    def test_analyze(self):
        for dialect in self.options["dialects"]:
            for script in self.options["scripts"]:
                if dialect == "Sorani" and script == "Arabic": 
                    stemmer = Stem("Sorani", "Arabic")
                    # print(dialect, script)
                    # test the morphological analyzer
                    for test_case in self.test_cases["analyze"][dialect][script]:
                        self.assertEqual(stemmer.analyze(test_case), self.test_cases["analyze"][dialect][script][test_case])
                    
                    # test the stemmer
                    for test_case in self.test_cases["stem"][dialect][script]:
                        for case in test_case["cases"]:
                            self.assertEqual(stemmer.stem(case, mark_unknown=test_case["parameters"]["mark_unknown"]), test_case["cases"][case])
                    
                    # test the lemmatizer
                    for test_case in self.test_cases["lemmatize"][dialect][script]:
                        # order of the lemmata may cause an error. Run many times.
                        self.assertEqual(stemmer.lemmatize(test_case), self.test_cases["lemmatize"][dialect][script][test_case])

                elif dialect == "Kurmanji" and script == "Latin":
                    stemmer = Stem("Kurmanji", "Latin")
                    # NOTICE: the order in which att_analyze returns morphological analyses may make these tests fail. Make sure the tests are run enough times.
                    for test_case in self.test_cases["analyze"][dialect][script]:
                        # print(test_case, stemmer.analyze(test_case))
                        self.assertEqual(stemmer.analyze(test_case), self.test_cases["analyze"][dialect][script][test_case])

                else: # otherwise, not supported currently
                    pass

if __name__ == "__main__":
    unittest.main()
