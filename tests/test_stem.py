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
                if (dialect == "Sorani" and script == "Arabic") or (
                        dialect == "Kurmanji" and script == "Latin"):  # otherwise, not supported currently
                    stemmer = Stem("Sorani", "Arabic")
                    # print(dialect, script)
                    for test_case in self.test_cases["analyze"][dialect][script]:
                        # print(test_case)
                        self.assertEqual(stemmer.analyze(test_case),
                                         self.test_cases["analyze"][dialect][script][test_case])


if __name__ == "__main__":
    unittest.main()
