#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Transliteration module of the Kurdish Language Processing Toolkit (KLPT).

    Based on the Wergor project: https://github.com/sinaahmadi/wergor
    Ahmadi, Sina. "A rule-based Kurdish text transliteration system." ACM Transactions on Asian and Low-Resource Language Information Processing (TALLIP) 18.2 (2019): 1-8.
    
    * created: 2020/06/12 02:13:26
    * author: Sina Ahmadi

"""

import sys
# sys.path.append('../klpt')
import itertools
import json
import re
from .preprocess import Preprocess
from .configuration import Configuration
import klpt

class Transliterate:
    """
    This module aims at transliterating one script of Kurdish into another one. Currently, only the Latin-based and the Arabic-based scripts of Sorani and Kurmanji are supported. The main function in this module is `transliterate()` which also takes care of detecting the correct form of double-usage graphemes, namely و ↔ w/u and ی ↔ î/y. In some specific occasions, it can also predict the placement of the missing *i* (also known as *Bizroke/بزرۆکە*).

    The module is based on the [Kurdish transliteration project](https://github.com/sinaahmadi/wergor).

    Example:
    ```python
    >>> from klpt.transliterate import Transliterate
    >>> transliterate = Transliterate("Kurmanji", "Latin", target_script="Arabic")
    >>> transliterate.transliterate("rojhilata navîn")
    'رۆژهلاتا ناڤین'

    >>> transliterate_ckb = Transliterate("Sorani", "Arabic", target_script="Latin")
    >>> transliterate_ckb.transliterate("لە وڵاتەکانی دیکەدا")
    'le wiłatekanî dîkeda'
    ```

    """

    def __init__(self, dialect, script, target_script, unknown="�", numeral="Latin"):
        """Initializing using a Configuration object

        To do:
            - "لە ئیسپانیا ژنان لە دژی ‘patriarkavirus’ ڕێپێوانیان کرد": "le îspanya jinan le dijî ‘patriarkavirus’ řêpêwanyan kird"
            - "egerçî damezrandnî rêkxrawe kurdîyekan her rêpênedraw mabûnewe Inzîbat.": "ئەگەرچی دامەزراندنی ڕێکخراوە کوردییەکان هەر رێپێنەدراو مابوونەوە ئنزیبات.",

        Args:
            mode ([type]): [description]
            unknown (str, optional): [description]. Defaults to "�".
            numeral (str, optional): [description]. Defaults to "Latin". Modifiable only if the source script is in Arabic. Otherwise, the Default value will be Latin.

        Raises:
            ValueError: [description]
            ValueError: [description]

        """
        # with open("data/default-options.json") as f:
        #     options = json.load(f)
        
        self.UNKNOWN = "�"
        with open(klpt.get_data("data/wergor.json"), encoding = "utf-8") as f:
            self.wergor_configurations = json.load(f)

        with open(klpt.get_data("data/preprocess_map.json"), encoding = "utf-8") as f:
            self.preprocess_map = json.load(f)["normalizer"]
        
        configuration = Configuration({"dialect": dialect, "script": script, "numeral": numeral, "target_script": target_script, "unknown": unknown})
        # self.preprocess_map = object.preprocess_map["normalizer"]
        self.dialect = configuration.dialect
        self.script = configuration.script
        self.numeral = configuration.numeral
        self.mode = configuration.mode
        self.target_script = configuration.target_script
        self.user_UNKNOWN = configuration.user_UNKNOWN

        # self.mode = mode
        # if mode=="arabic_to_latin":
        #     target_script = "Latin"
        # elif mode=="latin_to_arabic":
        #     target_script = "Arabic"
        # else:
        #     raise ValueError(f'Unknown transliteration option. Available options: {options["transliterator"]}')
    
        # if len(unknown):
        #     self.user_UNKNOWN = unknown
        # else:
        #     raise ValueError(f'Unknown unknown tag. Select a non-empty token (e.g. <UNK>.')

        self.characters_mapping = self.wergor_configurations["characters_mapping"]
        self.digits_mapping = self.preprocess_map["universal"]["numerals"][self.target_script]
        self.digits_mapping_all = list(set(list(self.preprocess_map["universal"]["numerals"][self.target_script].keys()) + list(self.preprocess_map["universal"]["numerals"][self.target_script].values())))
        self.punctuation_mapping = self.wergor_configurations["punctuation"][self.target_script]
        self.punctuation_mapping_all = list(set(list(self.wergor_configurations["punctuation"][self.target_script].keys()) + 
                                                list(self.wergor_configurations["punctuation"][self.target_script].values())))
        # self.tricky_characters = self.wergor_configurations["characters_mapping"]
        self.wy_mappings = self.wergor_configurations["wy_mappings"]

        self.hemze = self.wergor_configurations["hemze"]
        self.bizroke = self.wergor_configurations["bizroke"]
        self.uw_iy_forms = self.wergor_configurations["uw_iy_forms"]
        self.target_char = self.wergor_configurations["target_char"]
        self.arabic_vowels = self.wergor_configurations["arabic_vowels"]
        self.arabic_cons = self.wergor_configurations["arabic_cons"]
        self.latin_vowels = self.wergor_configurations["latin_vowels"]
        self.latin_cons = self.wergor_configurations["latin_cons"]
        
        self.characters_pack = {"arabic_to_latin": self.characters_mapping.values(), "latin_to_arabic": self.characters_mapping.keys()}
        if self.target_script == "Arabic":
            self.prep = Preprocess("Sorani", "Latin", numeral=self.numeral)
        else:
            self.prep = Preprocess("Sorani", "Latin", numeral="Latin")


    def to_pieces(self, token):
        """Given a token, find other segments composed of numbers and punctuation marks not seperated by space ▁""" 
        tokens_dict = dict()
        flag = False # True if a token is a \w
        i = 0

        for char_index in range(len(token)):
            if token[char_index] in self.digits_mapping_all or token[char_index] in self.punctuation_mapping_all:
                tokens_dict[char_index] = token[char_index]
                flag = False
                i = 0
            elif token[char_index] in self.characters_pack[self.mode] or \
                token[char_index] in self.target_char or \
                token[char_index] == self.hemze or token[char_index].lower() == self.bizroke:
                if flag:
                    tokens_dict[char_index-i] = tokens_dict[char_index-i] + token[char_index]
                else:
                    tokens_dict[char_index] = token[char_index]
                flag = True
                i += 1
            else:
                tokens_dict[char_index] = self.UNKNOWN
        
        return tokens_dict

    def transliterate(self, text):
        """The main method of the class:

        - find word boundaries by splitting it using spaces and then retrieve words mixed with other characters (without space)
        - map characters
        - detect double-usage characters w/u and y/î
        - find possible position of Bizroke (to be completed - 2017)

        Notice: text format should not be changed at all (no lower case, no style replacement \t, \n etc.).
        If the source and the target scripts are identical, the input text should be returned without any further processing.

        """
        text = self.prep.unify_numerals(text).split("\n")
        transliterated_text = list()

        for line in text:
            transliterated_line = list()
            for token in line.split():
                trans_token = ""
                # try:
                token = self.preprocessor(token) # This is not correct as the capital letter should be kept the way it is given.
                tokens_dict = self.to_pieces(token)
                # Transliterate words
                for token_key in tokens_dict:
                    if len(tokens_dict[token_key]):
                        word = tokens_dict[token_key]
                        if self.mode == "arabic_to_latin":
                            # w/y detection based on the priority in "word"
                            for char in word:
                                if char in self.target_char:
                                    word = self.uw_iy_Detector(word, char)  
                            if word[0] == self.hemze and word[1] in self.arabic_vowels:
                                word = word[1:]
                            word = list(word)
                            for char_index in range(len(word)):
                                word[char_index] = self.arabic_to_latin(word[char_index])
                            word = "".join(word)
                            word = self.bizroke_finder(word)
                        elif self.mode == "latin_to_arabic":
                            if len(word):
                                word = list(word)
                                for char_index in range(len(word)):
                                    word[char_index] = self.latin_to_arabic(word[char_index])
                                if word[0] in self.arabic_vowels or word[0].lower() == self.bizroke:
                                    word.insert(0, self.hemze)
                                word = "".join(word).replace("û", "وو").replace(self.bizroke.lower(), "").replace(self.bizroke.upper(), "")
                            # else:
                            #     return self.UNKNOWN

                        trans_token = trans_token + word
            
                transliterated_line.append(trans_token)
            transliterated_text.append(" ".join(transliterated_line).replace(u" w ", u" û "))

        # standardize the output
        # replace UNKOWN by the user's choice
        if self.user_UNKNOWN != self.UNKNOWN:
            return "\n".join(transliterated_text).replace(self.UNKNOWN, self.user_UNKNOWN)
        else:
            return "\n".join(transliterated_text)

    def preprocessor(self, word):
        """Preprocessing by normalizing text encoding and removing embedding characters"""
        # replace this by the normalization part
        word = list(word.replace('\u202b', "").replace('\u202c', "").replace('\u202a', "").replace(u"وو", "û").replace("\u200c", "").replace("ـ", ""))
        # for char_index in range(len(word)):
        #     if(word[char_index] in self.tricky_characters.keys()):
        #         word[char_index] = self.tricky_characters[word[char_index]]
        return "".join(word)

    def uw_iy_Detector(self, word, target_char):
        """Detection of "و" and "ی" in the Arabic-based script"""
        word = list(word)
        if target_char == "و":
            dic_index = 1
        else:
            dic_index = 0
        
        if word == target_char:
            word = self.uw_iy_forms["target_char_cons"][dic_index]
        else:
            for index in range(len(word)):
                if word[index] == self.hemze and word[index+1] == target_char:
                    word[index+1] = self.uw_iy_forms["target_char_vowel"][dic_index]
                    index += 1
                else:
                    if word[index] == target_char:
                        if index == 0:
                            word[index] = self.uw_iy_forms["target_char_cons"][dic_index]
                        else:
                            if word[index-1] in self.arabic_vowels:
                                word[index] = self.uw_iy_forms["target_char_cons"][dic_index]
                            else:
                                if index+1 < len(word):
                                    if word[index+1] in self.arabic_vowels:
                                        word[index] = self.uw_iy_forms["target_char_cons"][dic_index]
                                    else:
                                        word[index] = self.uw_iy_forms["target_char_vowel"][dic_index]
                                else:
                                    word[index] = self.uw_iy_forms["target_char_vowel"][dic_index]

        word = "".join(word).replace(self.hemze+self.uw_iy_forms["target_char_vowel"][dic_index], self.uw_iy_forms["target_char_vowel"][dic_index])
        return word

    def syllable_detector(self, word):
        """Detection of the syllable based on the given pattern. May be used for transcription applications."""
        syllable_templates = ["V", "VC", "VCC", "CV", "CVC", "CVCCC"]
        CV_converted_list = ""       
        for char in word:
            if char in self.latin_vowels:
                CV_converted_list += "V"
            else:
                CV_converted_list += "C"
        
        syllables = list()
        for i in range(1, len(CV_converted_list)):
            syllable_templates_permutated = [p for p in itertools.product(syllable_templates, repeat=i)]
            for syl in syllable_templates_permutated:
                if len("".join(syl)) == len(CV_converted_list):
                    if CV_converted_list == "".join(syl) and "VV" not in "".join(syl):
                        syllables.append(syl)
        return syllables

    def bizroke_finder(self, word):
        """Detection of the "i" character in the Arabic-based script. Incomplete version."""
        word = list(word)
        if len(word) > 2 and word[0] in self.latin_cons and word[1] in self.latin_cons and word[1] != "w" and word[1] != "y":
            word.insert(1, "i")
        return "".join(word)

    def arabic_to_latin(self, char):
        """Mapping Arabic-based characters to the Latin-based equivalents"""
        if char != "":
            if char in list(self.characters_mapping.values()):
                return list(self.characters_mapping.keys())[list(self.characters_mapping.values()).index(char)]
            elif char in self.punctuation_mapping:
                return self.punctuation_mapping[char]
            elif char in self.punctuation_mapping:
                return self.punctuation_mapping[char]
        return char

    def latin_to_arabic(self, char):
        """Mapping Latin-based characters to the Arabic-based equivalents"""
        # check if the character is in upper case
        mapped_char = ""
        
        if char.lower() != "":
            if char.lower() in self.wy_mappings.keys():
                mapped_char = self.wy_mappings[char.lower()]
            elif char.lower() in self.characters_mapping.keys():
                mapped_char = self.characters_mapping[char.lower()]
            elif char.lower() in self.punctuation_mapping:
                mapped_char = self.punctuation_mapping[char.lower()]
            # elif char.lower() in self.digits_mapping.values():
            #     mapped_char = self.digits_mapping.keys()[self.digits_mapping.values().index(char.lower())]
        
        if len(mapped_char):
            if char.isupper():
                return mapped_char.upper()
            return mapped_char
        else:
            return char


# Known bugs:
# لە ئیسپانیان ژنان لەدژی ‘patriarkavirus’ ڕێپێوانیان ئەنجامدا
# code mixed should not result an error!
# added this to the test cases. Moreover, you should fix the standardizing step after the task and preprocessing before the task
# Saza'm ne kevnar e
# Ez hîne yê bêzar im
# dwayîn zanyarî lebarey vayrosî koronay nwê (���î�-19)
# not able to transliterate words starting with capital letters : Berîtanya
