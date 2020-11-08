#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" The stemming module of the Kurdish Language Processing Toolkit (KLPT).

Based on the Hunspell implementation of Sorani Kurdish by Sina Ahmadi (2020)
    * created: 2020/07/12 02:58:26
    * author: Sina Ahmadi

"""

import sys
from hunspell import Hunspell
# from klpt.configuration import Configuration
sys.path.append('../klpt')
import klpt

class Stem():
    """The Stem class deals with various tasks as follows:
        - spell error detection and correction
        - morphological analysis
        - stemming

        These tasks are carried out in the `Kurdish Hunspell project <https://github.com/sinaahmadi/KurdishHunspell>`_.

    """

    def __init__(self, dialect, script):
        self.hunspell_flags = {"po": "pos", "is": "description", "ts": "terminal_suffix", "ds": "formation"}
        if dialect == "Sorani" and script == "Arabic":
            self.huns = Hunspell("ckb-Arab", hunspell_data_dir=klpt.get_data("data/"))
        else:
            raise Exception("Sorry, only Sorani dialect in the Arabic script is supported now. Stay tuned for other dialects and scripts!")

    # def stem(self, word):
    #     """A function for stemming a single word"""
    #     pass

    # def lemmatize(self, word):
    #     """A function for lemmatization of a single word"""
    #     pass

    def check_spelling(self, word):
        """Check spelling of a word

        Args:
            word (str): input word to be spell-checked

        Raises:
            TypeError: only string as input

        Returns:
            bool: True if the spelling is correct, False if the spelling is incorrect
        """
        if not isinstance(word, str):
            raise TypeError("Only a word (str) is allowed.")
        else:
            return self.huns.spell(word)

    def correct_spelling(self, word):
        """Correct spelling errors if the input word is incorrect

        Args:
            word (str): input word to be spell-checked

        Raises:
            TypeError: only string as input

        Returns:
            tuple (boolean, list): a tuple where the first element indicates the correctness of the word (True if correct, False if incorrect).
            If the input word is incorrect, suggestions are provided in a list as the second element of the tuple, as (False, []).
            If no suggestion is available, the list is returned empty as (True, []).
        """
        if not isinstance(word, str):
            raise TypeError("Only a word (str) is allowed.")
        else:
            if self.check_spelling(word):
                return (True, [])
            return (False, list(self.huns.suggest(word)))

    def analyze(self, word_form):
        """Morphological analysis of a given word
        More details regarding Kurdish morphological analysis can be found at https://github.com/sinaahmadi/KurdishHunspell

        Args:
            word_form (str): a single word-form

        Raises:
            TypeError: only string as input

        Returns:
            (list(dict)): a list of all possible morphological analyses according to the defined morphological rules
            
            The morphological analysis is returned as a dictionary as follows:
             - "pos": the part-of-speech of the word-form according to `the Universal Dependency tag set <https://universaldependencies.org/u/pos/index.html>`_ 
             - "description": is flag
             - "terminal_suffix": anything except ts flag
             - "formation": if ds flag is set, its value is assigned to description and the value of formation is set to derivational. Although the majority of our morphological rules cover inflectional forms, it is not accurate to say all of them are inflectional. Therefore, we only set this value to derivational wherever we are sure.
             - "base": `ts` flag. The definition of terminal suffix is a bit tricky in Hunspell. According to `the Hunspell documentation <http://manpages.ubuntu.com/manpages/trusty/en/man4/hunspell.4.html>`_, "Terminal suffix fields are inflectional suffix fields "removed" by additional (not terminal) suffixes". In other words, the ts flag in Hunspell represents whatever is left after stripping all affixes. Therefore, it is the morphological base.

            If the input cannot be analyzed morphologically, an empty list is returned.
        """
        if not isinstance(word_form, str):
            raise TypeError("Only a word (str) is allowed.")
        else:
            # Given the morphological analysis of a word-form with Hunspell flags, extract relevant information and return a dictionary
            word_analysis = list()
            for analysis in list(self.huns.analyze(word_form)):
                analysis_dict = dict()
                for item in analysis.split():
                    if ":" not in item:
                        continue
                    if item.split(":")[1] == "ts":
                        # ts flag exceptionally appears after the value as value:key in the Hunspell output
                        analysis_dict["base"] = item.split(":")[0]
                        # anything except the terminal_suffix is considered to be the base
                        analysis_dict[self.hunspell_flags[item.split(":")[1]]] = word_form.replace(item.split(":")[0], "")
                    elif item.split(":")[0] in self.hunspell_flags.keys():
                        # assign the key:value pairs from the Hunspell string output to the dictionary output of the current function
                        # for ds flag, add derivation as the formation type, otherwise inflection
                        if item.split(":")[0] == "ds":
                            analysis_dict[self.hunspell_flags[item.split(":")[0]]] = "derivational"
                            analysis_dict[self.hunspell_flags["is"]] = item.split(":")[1]
                        else:
                            analysis_dict[self.hunspell_flags[item.split(":")[0]]] = item.split(":")[1]

                # if there is no value assigned to the ts flag, the terminal suffix is a zero-morpheme 0
                if self.hunspell_flags["ts"] not in analysis_dict or analysis_dict[self.hunspell_flags["ts"]] == "":
                    analysis_dict[self.hunspell_flags["ts"]] = "0"

                word_analysis.append(analysis_dict)

        return word_analysis
