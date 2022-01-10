#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../klpt')
import unittest
from klpt.tokenize import Tokenize
import json
import klpt

class TestTokenize(unittest.TestCase):
    """ Test unit for the Preprocess class"""
    def setUp(self):
        with open(klpt.get_data("data/test_cases_tokenize.json"), encoding = "utf-8") as f:
            self.test_cases = json.load(f)
                    
        with open(klpt.get_data("data/default-options.json"), encoding = "utf-8") as f:
            self.options = json.load(f)

    def tearDown(self):
        pass

    def test_mwe_tokenize(self):
        for dialect in self.options["dialects"]:
            for script in self.options["scripts"]:
                if (dialect == "Sorani" and script == "Arabic") or (dialect == "Kurmanji" and script == "Latin"): # otherwise, not supported currently
                    # print(dialect, script)
                    tokenizer = Tokenize(dialect, script)
                    for test_case in self.test_cases["mwe_tokenize"][dialect][script]:
                        for case in test_case["cases"]:
                            # print(case, test_case["parameters"]["separator"], test_case["parameters"]["in_separator"], test_case["parameters"]["punct_marked"])
                            self.assertCountEqual(tokenizer.mwe_tokenize(case, separator=test_case["parameters"]["separator"],
                                                                            in_separator=test_case["parameters"]["in_separator"],
                                                                            punct_marked=test_case["parameters"]["punct_marked"],
                                                                            keep_form=test_case["parameters"]["keep_form"]),
                                                                            test_case["cases"][case])

    def test_sent_tokenize(self):
        for dialect in self.options["dialects"]:
            for script in self.options["scripts"]:
                if (dialect == "Sorani" and script == "Arabic") or (dialect == "Kurmanji" and script == "Latin"): # otherwise, not supported currently
                    for case in self.test_cases["sent_tokenize"][dialect][script]:
                        tokenizer = Tokenize(dialect, script)
                        # print(case)
                        self.assertCountEqual(tokenizer.sent_tokenize(case), self.test_cases["sent_tokenize"][dialect][script][case])

if __name__ == "__main__":
    unittest.main()