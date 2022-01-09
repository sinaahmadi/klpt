#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../klpt')
import unittest
from klpt.preprocess import Preprocess
import klpt
import json


class TestPreprocess(unittest.TestCase):
    """ Test unit for the Preprocess class"""
    def setUp(self):
        with open(klpt.get_data("data/test_cases.json"), encoding = "utf-8") as f:
            self.test_cases = json.load(f)
                    
        with open(klpt.get_data("data/default-options.json"), encoding = "utf-8") as f:
            self.options = json.load(f)

    def tearDown(self):
        pass

    def test_normalizer(self):
        for dialect in self.options["dialects"]:
            for script in self.options["scripts"]:
                for case in self.test_cases["normalizer"][dialect][script]:
                    prep = Preprocess(dialect, script)
                    # print(case, prep.normalizer(case))
                    self.assertCountEqual(prep.normalize(case), self.test_cases["normalizer"][dialect][script][case])

    def test_standardizer(self):
        # print("standardization")
        for dialect in self.options["dialects"]:
            for script in self.options["scripts"]:
                for case in self.test_cases["standardizer"][dialect][script]:
                    prep = Preprocess(dialect, script)
                    # print(case, prep.standardizer(case))
                    self.assertCountEqual(prep.standardize(case), self.test_cases["standardizer"][dialect][script][case])

    def test_unify_numerals(self):
        # print("unify numerals")
        for numeral in self.options["numerals"]:
            for case in self.test_cases["numerals"][numeral]:
                prep = Preprocess("Sorani", "Latin", numeral)
                self.assertCountEqual(prep.unify_numerals(case), self.test_cases["numerals"][numeral][case])

    def test_stopwords(self):
        # print("stopwords")
        for dialect in self.options["dialects"]:
            for script in self.options["scripts"]:
                for case in self.test_cases["stopwords"][dialect][script]:
                    prep = Preprocess(dialect, script)
                    self.assertCountEqual([token for token in case.split() if token not in prep.stopwords], self.test_cases["stopwords"][dialect][script][case])

if __name__ == "__main__":
    unittest.main()