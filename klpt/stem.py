#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" The stemming module of the Kurdish Language Processing Toolkit (KLPT).

Based on the Hunspell implementation of Sorani Kurdish by Sina Ahmadi (2020)
    * created: 2020/07/12 02:58:26
    * author: Sina Ahmadi

"""

import sys
from hunspell import Hunspell
from klpt.att_analyze import Analysis
from klpt.configuration import Configuration
sys.path.append('../klpt')
import klpt

class Stem:
    """

    The Stem module deals with various tasks, mainly through the following functions:
        - `check_spelling`: spell error detection
        - `correct_spelling`: spell error correction
        - `analyze`: morphological analysis

    Please note that only Sorani is supported in this version in this module. The module is based on the [Kurdish Hunspell project](https://github.com/sinaahmadi/KurdishHunspell).

    Example:
    ```python
    >>> from klpt.stem import Stem
    >>> stemmer = Stem("Sorani", "Arabic")
    >>> stemmer.check_spelling("سوتاندبووت")
    False
    >>> stemmer.correct_spelling("سوتاندبووت")
    (False, ['ستاندبووت', 'سووتاندبووت', 'سووڕاندبووت', 'ڕووتاندبووت', 'فەوتاندبووت', 'بووژاندبووت'])
    >>> stemmer.analyze("دیتبامن")
    [{'pos': 'verb', 'description': 'past_stem_transitive_active', 'base': 'دیت', 'terminal_suffix': 'بامن'}]
    >>> stemmer.stem("دەچینەوە")
    ['چ']
    
    >>> stemmer = Stem("Kurmanji", "Latin")
    >>> stemmer.analyze("dibêjim")
    [{'base': 'gotin', 'description': 'vblex_tv_pri_p1_sg', 'pos': '', 'terminal_suffix': '', 'formation': ''}]
    ```

    """

    def __init__(self, dialect, script):

        self.dialect = dialect
        self.script = script 

        self.hunspell_flags = {"po": "pos", "is": "description", "ts": "terminal_suffix", "ds": "formation", "st": "stem"}
        if self.dialect == "Sorani" and self.script == "Arabic":
            self.huns = Hunspell("ckb-Arab", hunspell_data_dir=klpt.get_data("data/"))
        else:
            if not (self.dialect == "Kurmanji" and self.script == "Latin"):
                raise Exception("Sorry, only Sorani dialect in the Arabic script and Kurmanji in the Latin script is supported now. Stay tuned for other dialects and scripts!")

    def stem(self, word):
        """A function for stemming a single word

        Args:
            word (str): input word to be spell-checked

        Raises:
            TypeError: only string as input

        Returns:
            list: list of stem(s)
        """
        if not isinstance(word, str) or not (self.dialect == "Sorani" and self.script == "Arabic"):
            raise TypeError("Not supported yet.")
        else:
            return list(set([self.clean_stem(i) for i in self.huns.stem(word)]))

    # def lemmatize(self, word):
    #     """A function for lemmatization of a single word"""
    #     pass
    def clean_stem(self, word):
        """Remove extra characters in the stem
        The following issue was observed when stemming with Hunspell (version 2.0.2) where
        the retrieved stem of a verb is accompanied by the flag of the word, which is an unwanted extra character.
        Possible flags are T, V and I. :lf should also be taken into account.

        Args:
            word ([str]): [stem]
        """
        for char in ["V", "I", "T"]:
            word = word.replace(char, "")
        return word.replace(":lf", "")

    def check_spelling(self, word):
        """Check spelling of a word

        Args:
            word (str): input word to be spell-checked

        Raises:
            TypeError: only string as input

        Returns:
            bool: True if the spelling is correct, False if the spelling is incorrect
        """
        if not isinstance(word, str) or not (self.dialect == "Sorani" and self.script == "Arabic"):
            raise TypeError("Not supported yet.")
        else:
            return self.huns.spell(word)

    def correct_spelling(self, word):
        """
        Correct spelling errors if the input word is incorrect. It returns a tuple where the first element indicates the correctness of the word (True if correct, False if incorrect).
            If the input word is incorrect, suggestions are provided in a list as the second element of the tuple, as (False, []).
            If no suggestion is available, the list is returned empty as (True, []).

        Args:
            word (str): input word to be spell-checked

        Raises:
            TypeError: only string as input

        Returns:
            tuple (boolean, list)

        """
        if not isinstance(word, str) or not (self.dialect == "Sorani" and self.script == "Arabic"):
            raise TypeError("Not supported yet.")
        else:
            if self.check_spelling(word):
                return (True, [])
            return (False, list(self.huns.suggest(word)))

    def analyze(self, word_form):
        """
        Morphological analysis of a given word.
        
        It returns morphological analyses. The morphological analysis is returned as a dictionary as follows:
        
        - "pos": the part-of-speech of the word-form according to [the Universal Dependency tag set](https://universaldependencies.org/u/pos/index.html). 
        - "description": is flag
        - "terminal_suffix": anything except ts flag
        - "st": the stem of the word
        - "formation": if ds flag is set, its value is assigned to description and the value of formation is set to derivational. Although the majority of our morphological rules cover inflectional forms, it is not accurate to say all of them are inflectional. Therefore, we only set this value to derivational wherever we are sure.
        - "base": `ts` flag. The definition of terminal suffix is a bit tricky in Hunspell. According to [the Hunspell documentation](http://manpages.ubuntu.com/manpages/trusty/en/man4/hunspell.4.html), "Terminal suffix fields are inflectional suffix fields "removed" by additional (not terminal) suffixes". In other words, the ts flag in Hunspell represents whatever is left after stripping all affixes. Therefore, it is the morphological base.

        As in [{'pos': 'verb', 'description': 'past_stem_transitive_active', 'base': 'دیت', 'terminal_suffix': 'بامن'}]
        If the input cannot be analyzed morphologically, an empty list is returned.

        Sorani: 
        More details regarding Sorani Kurdish morphological analysis can be found at [https://github.com/sinaahmadi/KurdishHunspell](https://github.com/sinaahmadi/KurdishHunspell).

        Kurmanji:
        Regarding Kurmanji, we use the morphological analyzer provided by the [Kurmanji part](https://github.com/apertium/apertium-kmr)

        Please note that there are delicate difference between who the analyzers work in Hunspell and Apertium. For instane, the `base` in the Kurmanji analysis refers to the lemma while in Sorani (from Hunspell), it refers to the morphological base.

        Args:
            word_form (str): a single word-form

        Raises:
            TypeError: only string as input

        Returns:
            (list(dict)): a list of all possible morphological analyses according to the defined morphological rules
            
        """
        if not isinstance(word_form, str):
            raise TypeError("Only a word (str) is allowed.")
        else:
            word_analysis = list()
            if self.dialect == "Sorani" and self.script == "Arabic":
                # Given the morphological analysis of a word-form with Hunspell flags, extract relevant information and return a dictionary
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
                            # TODO: prefixes and suffixes are merged together as ts. To be separated.  
                        elif item.split(":")[0] in self.hunspell_flags.keys():
                            # assign the key:value pairs from the Hunspell string output to the dictionary output of the current function
                            # for ds flag, add derivation as the formation type, otherwise inflection
                            if item.split(":")[0] == "ds":
                                analysis_dict[self.hunspell_flags[item.split(":")[0]]] = "derivational"
                                analysis_dict[self.hunspell_flags["is"]] = item.split(":")[1]
                            # for st flag, stem should be cleaned first
                            elif item.split(":")[0] == "st":
                                analysis_dict[self.hunspell_flags[item.split(":")[0]]] = self.clean_stem(item.split(":")[1])
                            else:
                                analysis_dict[self.hunspell_flags[item.split(":")[0]]] = item.split(":")[1]

                    # if there is no value assigned to the ts flag, the terminal suffix is a zero-morpheme 0
                    if self.hunspell_flags["ts"] not in analysis_dict or analysis_dict[self.hunspell_flags["ts"]] == "":
                        analysis_dict[self.hunspell_flags["ts"]] = "0"

                    word_analysis.append(analysis_dict)

            elif self.dialect == "Kurmanji" and self.script == "Latin":
                att_analysis = Analysis("Kurmanji", "Latin").analyze(word_form)

                # check if the word-form is analyzed or no
                if not len(att_analysis):
                    # the word-form could not be analyzed
                    return []

                for analysis in att_analysis:
                    analysis_dict = dict()
                    structure = analysis[0].split("<", 1)
                    analysis_dict["base"], analysis_dict["description"] = structure[0], structure[1].replace("><", "_").replace(">", "").strip()
                    analysis_dict["pos"] = ""
                    analysis_dict["terminal_suffix"] = ""
                    analysis_dict["formation"] = ""
                    # TODO: the description needs further information extraction in such a way that some values should be assigned to the "pos" key 
                    # analysis_dict["terminal_suffix"] = word_form.replace(analysis_dict["base"], "")
                    word_analysis.append(analysis_dict)

        return word_analysis