#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../klpt')
import json
# from klpt.preprocess import Preprocess
# from klpt.transliterator import Transliterator
# from klpt.configuration import Configuration

__url__ = "https://sinaahmadi.github.io/klpt"

# Maintainer, contributors, etc.
__maintainer__ = "Sina Ahmadi"
__maintainer_email__ = "ahmadi.sina@outlook.com"
__author__ = __maintainer__
__author_email__ = __maintainer_email__

# with open("data/stopwords.json") as f:
#         stopwords = json.load(f)[self.dialect][self.script]
# if __name__ == "__main__":

# def remove_stopwords(self, text):
#         """remove stopwords"""
#         return " ".join([token for token in text.split() if token not in self.stopwords])

data_directory = {
    "tokenize": {
        "Sorani": {
            "Arabic": "data/lexicon_ckb_arab.json",
            "Latin": "data/lexicon_ckb_latn.json"
            },
        "Kurmanji": {
            "Latin": "data/lexicon_kmr_latn.json"
        }
    },
    "morphemes": {
        "Sorani": "data/ckb-morphemes.json",
        "Kurmanji": "data/kmr-morphemes.json"
    }
}