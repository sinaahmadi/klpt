#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Preprocessing module of the Kurdish Language Processing Toolkit (KLPT).

    Normalizing scripts and orthographies by using writing conventions based on dialects and scripts.
    The goal is not to correct the orthography but to normalize the text in terms of the encoding and common writing rules.

        * created: 2020/05/10 02:10:54
        * author: Sina Ahmadi
    
"""

import json
import re
import sys
from .configuration import Configuration
sys.path.append('../klpt')
import klpt

class Preprocess:
    """
    This module deals with normalizing scripts and orthographies by using writing conventions based on dialects and scripts. The goal is not to correct the orthography but to normalize the text in terms of the encoding and common writing rules. The input encoding should be in UTF-8 only. To this end, three functions are provided as follows:

    - `normalize`: deals with different encodings and unifies characters based on dialects and scripts
    - `standardize`: given a normalized text, it returns standardized text based on the Kurdish orthographies following recommendations for [Kurmanji](https://books.google.ie/books?id=Z7lDnwEACAAJ) and [Sorani](http://yageyziman.com/Renusi_Kurdi.htm)
    - `unify_numerals`: conversion of the various types of numerals used in Kurdish texts
    - `preprocess`: one single function for normalization, standardization and unification of numerals

    In addition, it is possible to remove stopwords using the `stopwords` variable. It is better to remove stopwords after the tokenization task.

    It is recommended that the output of this module be used as the input of subsequent tasks in an NLP pipeline.
    
    Example:

    ```python
    >>> from klpt.preprocess import Preprocess

    >>> preprocessor_ckb = Preprocess("Sorani", "Arabic", numeral="Latin")
    >>> preprocessor_ckb.normalize("لە ســـاڵەکانی ١٩٥٠دا")
    'لە ساڵەکانی 1950دا'
    >>> preprocessor_ckb.standardize("راستە لەو ووڵاتەدا")
    'ڕاستە لەو وڵاتەدا'
    >>> preprocessor_ckb.unify_numerals("٢٠٢٠")
    '2020'
    >>> preprocessor_ckb.preprocess("راستە لە ووڵاتەی ٢٣هەمدا")
    'ڕاستە لە وڵاتەی 23هەمدا'

    >>> preprocessor_kmr = Preprocess("Kurmanji", "Latin")
    >>> preprocessor_kmr.standardize("di sala 2018-an")
    'di sala 2018an'
    >>> preprocessor_kmr.standardize("hêviya")
    'hêvîya'
    >>> preprocessor_kmr.stopwords[:10]
    ['a', 'an', 'bareya', 'bareyê', 'barên', 'basa', 'be', 'belê', 'ber', 'bereya']
    ```

    The preprocessing rules are provided at [`data/preprocess_map.json`](https://github.com/sinaahmadi/klpt/blob/master/klpt/data/preprocess_map.json).
    """

    def __init__(self, dialect, script, numeral="Latin"):
        """
        Initialization of the Preprocess class

        Arguments:
            dialect (str): the name of the dialect or its ISO 639-3  code
            script (str): the name of the script
            numeral (str): the type of the numeral
        
        """
        with open(klpt.get_data("data/preprocess_map.json"), encoding = "utf-8") as preprocess_file:
            self.preprocess_map = json.load(preprocess_file)

        configuration = Configuration({"dialect": dialect, "script": script, "numeral": numeral})
        self.dialect = configuration.dialect
        self.script = configuration.script
        self.numeral = configuration.numeral
        # self.preprocess_map = config.preprocess_map

        with open(klpt.data_directory["stopwords"], "r", encoding = "utf-8") as f:
            self.stopwords = json.load(f)[dialect][script]

    def standardize(self, text):
        """
        Method of standardization of Kurdish orthographies

        Given a normalized text, it returns standardized text based on the Kurdish orthographies.

        - Sorani-Arabic:
            - replace alveolar flap ر (/ɾ/) at the begging of the word by the alveolar trill ڕ (/r/)
            - replace double rr and ll with ř and ł respectively

        - Kurmanji-Latin:
            - replace "-an" or "'an" in dates and numerals ("di sala 2018'an" and "di sala 2018-an" -> "di sala 2018an")

        Open issues:
            - replace " وە " by  " و "? But this is not always possible, "min bo we" (ریزگـرتنا من بو وە  نە ئە وە ئــە ز)
            - "pirtükê": "pirtûkê"?
            - Should [ı (LATIN SMALL LETTER DOTLESS I](https://www.compart.com/en/unicode/U+0131) be replaced by i?

        Arguments:
            text (str): a string

        Returns:
            str: standardized text

        """
        temp_text = " " + self.unify_numerals(text) + " "

        for standardization_type in [self.dialect]:
            for rep in self.preprocess_map["standardizer"][standardization_type][self.script]:
                rep_tar = self.preprocess_map["standardizer"][standardization_type][self.script][rep]
                temp_text = re.sub(rf"{rep}", rf"{rep_tar}", temp_text, flags=re.I)

        return temp_text.strip()

    def normalize(self, text):
        """
        Text normalization

        This function deals with different encodings and unifies characters based on dialects and scripts as follows:
        
        - Sorani-Arabic:
        
            - replace frequent Arabic characters with their equivalent Kurdish ones, e.g. "ي" by "ی" and "ك" by "ک"
            - replace "ه" followed by zero-width non-joiner (ZWNJ, U+200C) with "ە" where ZWNJ is removed ("ره‌زبه‌ر" is converted to "رەزبەر"). ZWNJ in HTML is also taken into account.
            - replace "هـ" with "ھ" (U+06BE, ARABIC LETTER HEH DOACHASHMEE)
            - remove Kashida "ـ"
            - "ھ" in the middle of a word is replaced by ه (U+0647)
            - replace different types of y, such as 'ARABIC LETTER ALEF MAKSURA' (U+0649)

        It should be noted that the order of the replacements is important. Check out provided files for further details and test cases.

        Arguments:
            text (str): a string

        Returns:
            str: normalized text

         """
        temp_text = " " + self.unify_numerals(text) + " "

        for normalization_type in ["universal", self.dialect]:
            for rep in self.preprocess_map["normalizer"][normalization_type][self.script]:
                rep_tar = self.preprocess_map["normalizer"][normalization_type][self.script][rep]
                temp_text = re.sub(rf"{rep}", rf"{rep_tar}", temp_text, flags=re.I)

        return temp_text.strip()

    def unify_numerals(self, text):
        """
        Convert numerals to the desired one

        There are three types of numerals:
        - Arabic [١٢٣٤٥٦٧٨٩٠]
        - Farsi [۱۲۳۴۵۶۷۸۹۰]
        - Latin [1234567890]

        Arguments:
            text (str): a string

        Returns:
            str: text with unified numerals

        """
        for i, j in self.preprocess_map["normalizer"]["universal"]["numerals"][self.numeral].items():
            text = text.replace(i, j)
        return text

    def preprocess(self, text):
        """
        One single function for normalization, standardization and unification of numerals

        Arguments:
            text (str): a string

        Returns:
            str: preprocessed text
        """
        return self.unify_numerals(self.standardize(self.normalize(text)))
