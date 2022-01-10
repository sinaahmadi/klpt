#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../klpt')
import unittest
from klpt.transliterate import Transliterate
import json
import klpt

class TestTransliterator(unittest.TestCase):
    """ Test unit for the Preprocess module"""
    def setUp(self):
        with open(klpt.get_data("data/test_cases.json"), encoding = "utf-8") as f:
            self.test_cases = json.load(f)
                    
        with open(klpt.get_data("data/default-options.json"), encoding = "utf-8") as f:
            self.options = json.load(f)

    def tearDown(self):
        pass

    def test_transliterator(self):
        for option in self.options["transliterator"] + ["unknown"]:
            if option != "unknown":

                if option == "arabic_to_latin":
                    source_script = "Arabic"
                    target_script = "Latin"
                else:
                    source_script = "Latin"
                    target_script = "Arabic"

                for numeral in self.test_cases["transliterator"][option]["numerals"]:
                    print(option, numeral)
                    for case in self.test_cases["transliterator"][option]["numerals"][numeral]:
                        wergor = Transliterate("Sorani", source_script, target_script, numeral=numeral)
                        self.assertCountEqual(wergor.transliterate(case), self.test_cases["transliterator"][option]["numerals"][numeral][case])
            else:
                for unk in self.test_cases["transliterator"][option]:
                    for case in self.test_cases["transliterator"][option][unk]:
                        wergor = Transliterate("Sorani", "Latin", "Arabic", unknown=unk)
                        self.assertCountEqual(wergor.transliterate(case), self.test_cases["transliterator"][option][unk][case])

                        wergor = Transliterate("Sorani", "Arabic", "Latin", unknown=unk)
                        self.assertCountEqual(wergor.transliterate(case), self.test_cases["transliterator"][option][unk][case])
    
if __name__ == "__main__":
    unittest.main()
