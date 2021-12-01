#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../klpt')
import os

__url__ = "https://sinaahmadi.github.io/klpt"

# Maintainer, contributors, etc.
__maintainer__ = "Sina Ahmadi"
__maintainer_email__ = "ahmadi.sina@outlook.com"
__author__ = __maintainer__
__author_email__ = __maintainer_email__

_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path):
    return os.path.join(_ROOT, '', path)

data_directory = {
    "tokenize": {
        "Sorani": {
            "Arabic": get_data("data/lexicon_ckb_arab.json"),
            "Latin": get_data("data/lexicon_ckb_latn.json")
            },
        "Kurmanji": {
            "Latin": get_data("data/lexicon_kmr_latn.json")
        }
    },
    "morphemes": {
        "Sorani": get_data("data/ckb-morphemes.json"),
        "Kurmanji": get_data("data/kmr-morphemes.json")
    },
    "analyser": {
        "Sorani": get_data("data/ckb-analyser.att"),
        "Kurmanji": get_data("data/kmr-analyser.att")
    },
    "stopwords": get_data("data/stopwords.json")
}