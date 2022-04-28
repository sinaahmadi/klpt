#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" The stemming module of the Kurdish Language Processing Toolkit (KLPT).

Based on the Hunspell implementation of Sorani Kurdish by Sina Ahmadi (2020)
    * created: 2020/07/12 02:58:26
    * author: Sina Ahmadi

"""

import sys
import json
from hunspell import Hunspell
from klpt.att_analyze import Analysis
from klpt.configuration import Configuration
sys.path.append('../klpt')
import klpt
from klpt import utility

class Stem:
    """

    The Stem module deals with various tasks, mainly through the following functions:
        - `check_spelling`: spell error detection
        - `correct_spelling`: spell error correction
        - `analyze`: morphological analysis
        - `stem`: stemming, e.g. "بڕاوە" → "بڕ"
        - `lemmatize`: lemmatization, e.g. "بردمنەوە" → "بردن"

    It is recommended that this module be used on tokens using the tokenization module. 
    Please note that only Sorani is supported in this version in this module. The module is based on the [Kurdish Hunspell project](https://github.com/sinaahmadi/KurdishHunspell).

    Regarding stemming, the following procedure is followed:
        - for tokens of a single word, as "kirin" (to do), the stem of the token is returned.
        - for compound forms and multi-word expressions, the stem of the noun, adjective or adverb are taken into account. For instance, in the light verbal constructions such as "bar kirin" (to load), the stem of the nominal component "bar" is returned. In other cases, the stem of that part of the MWE token is returned that is semantically more important, as in "دەست تێ وەردان" (dest-tê-werdan) where the stem of "dest" is returned.

    Example:
    ```python
    >>> from klpt.stem import Stem
    >>> stemmer = Stem("Sorani", "Arabic")
    >>> stemmer.check_spelling("سوتاندبووت")
    False
    >>> stemmer.correct_spelling("سوتاندبووت")
    (False, ['ستاندبووت', 'سووتاندبووت', 'سووڕاندبووت', 'ڕووتاندبووت', 'فەوتاندبووت', 'بووژاندبووت'])
    >>> stemmer.analyze("دیتبامن")
    [{'pos': ['verb'], 'description': 'past_stem_transitive_active', 'stem': 'دی', 'lemma': ['دیتن'], 'base': 'دیت', 'prefixes': '', 'suffixes': 'بامن'}]
    >>> stemmer.stem("دەچینەوە")
    ['چ']
    >>> stemmer.stem("گورەکە", mark_unknown=True)
    ['_گور_']
    >>> stemmer.lemmatize("گوڵەکانم")
    ['گوڵ', 'گوڵە']
    
    >>> stemmer = Stem("Kurmanji", "Latin")
    >>> stemmer.analyze("dibêjim")
    [{'base': 'gotin', 'description': 'vblex_tv_pri_p1_sg', 'pos': '', 'terminal_suffix': '', 'formation': ''}]
    ```

    """
    # to do: make the following function work for Kurmanji Latin also following the same algorithm
    def __init__(self, dialect, script):

        self.dialect = dialect
        self.script = script 

        self.hunspell_flags = {"po": "pos", "is": "description", "ds": "formation", "st": "stem", "lem": "lemma"}
        
        if self.dialect == "Sorani" and self.script == "Arabic":
            self.huns = Hunspell("ckb-Arab", hunspell_data_dir=klpt.get_data("data/"))
            with open(klpt.data_directory["morphemes"][self.dialect], "r", encoding = "utf-8") as f_morphemes:
                self.light_verbs = json.load(f_morphemes)["Morphemes"]["light_verbs"][self.script]
        elif self.dialect == "Kurmanji" and self.script == "Latin":
            self.huns = Hunspell("kmr-Latn", hunspell_data_dir=klpt.get_data("data/"))
            with open(klpt.data_directory["morphemes"][self.dialect], "r", encoding = "utf-8") as f_morphemes:
                self.light_verbs = json.load(f_morphemes)["Morphemes"]["light_verbs"][self.script]
        else:
            raise Exception("Sorry, only Sorani dialect in the Arabic script and Kurmanji in the Latin script is supported now. Stay tuned for other dialects and scripts!")
            
        with open(klpt.data_directory["morphemes"][self.dialect], "r", encoding = "utf-8") as f_morphemes:
            self.morphemes = json.load(f_morphemes)["Morphemes"]["Concatenated"][self.script]

    def stem(self, word, mark_unknown=False):
        """A function for stemming a single word

        Args:
            word (str): input word to be spell-checked
            mark_unknown (False): if the given word is unknown in the tagged lexicon, KLPT stems is following rules. Such stems can be marked with "_" if this variable set to True

        Raises:
            TypeError: only string as input

        Returns:
            list: list of stem(s)
        """
        if not isinstance(word, str):
            raise TypeError("Not supported yet.")
        elif (self.dialect == "Sorani" and self.script == "Arabic") or (self.dialect == "Kurmanji" and self.script == "Latin"):
            stems = list(set([self.clean_stem(i) for i in self.huns.stem(word)]))
            if len(stems):
                return stems
            else:
                # not detected by Hunspell or the word doesn't exist in the tagged lexicon
                for verb in self.light_verbs:
                    if word.endswith(verb) and len(word.rpartition(verb)[0]):
                        stems = list(set([self.clean_stem(i) for i in self.huns.stem(word.rpartition(verb)[0].strip())]))
                        if len(stems):
                            # the word is a compound form with a light verb. The other part can be stemmed by Hunspell
                            return stems
                        else:
                            # the word is a compound form with a light verb but the other part cannot be stemmed by Hunspell
                            word = word.rpartition(verb)[0].strip()
                
                # the other part of the word or the whole word cannot be stemmed by Hunspell
                # so, find the stem following morphological rules by checking if removing possible prefixes and suffixes would help finding the stem.
                # Note: even though the same morphemes used in the tokenization system are used in the rules here, there is a delicate difference.
                #    In the tokenization system, the trimming is done in such a way that shorter morphemes are first checked for suffixes (suffixes in the json file is sorted by length) and longer prefixes are trimmed first.
                #    For the stemmer, however, we do differently by first checking the longer morphemes then shorter ones (for both prefixes and suffixes). 
                #    This is due to the different purposes of the two tasks. Therefore, the list of the morphemes is to be reversed for suffixes (not prefixes). 
                # In order not to modify the json files, the `reversed` function is used for suffixes.
                
                for preposition in self.morphemes["prefixes"]:
                    if word.startswith(preposition) and len(word.split(preposition, 1)) > 1:
                        if len(list(set([self.clean_stem(i) for i in self.huns.stem(word.split(preposition, 1)[1])]))):
                            stems = list(set([self.clean_stem(i) for i in self.huns.stem(word.split(preposition, 1)[1])]))
                            if mark_unknown:
                                return ["_" + i + "_" for i in stems]
                        else:
                            word = word.split(preposition, 1)[1]
                            break
                
                for postposition in reversed(list(self.morphemes["suffixes"])):
                    if word.endswith(postposition) and len(word.rpartition(postposition)[0]):
                        if len(list(set([self.clean_stem(i) for i in self.huns.stem(word.rpartition(postposition)[0])]))):
                            stems = list(set([self.clean_stem(i) for i in self.huns.stem(word.rpartition(postposition)[0])]))
                            if mark_unknown:
                                return ["_" + i + "_" for i in stems]
                        else:
                            word = word.rpartition(postposition)[0]
                            break
                
                # not possible to stem the word using the tagged lexicon or the rule-based approach. Return the word as it is.
                if mark_unknown:
                    return ["_" + word + "_"]
                else:
                    return [word]

    def lemmatize(self, word):
        """A function for lemmatization of words

        Args:
            word ([str]): [given a word, return its lemma form, i.e. dictionary entry form]
        
        Raises:
            TypeError: only string as input

        Returns:
            list: list of lemma(s)
        """
        if not isinstance(word, str):
            raise TypeError("Not supported yet.")
        elif (self.dialect == "Sorani" and self.script == "Arabic") or (self.dialect == "Kurmanji" and self.script == "Latin"):
            word_analysis = self.analyze(word)
            return list(set([item for sublist in word_analysis for item in sublist["lemma"] if item != '']))

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
        if not isinstance(word, str):
            raise TypeError("Not supported yet.")
        elif (self.dialect == "Sorani" and self.script == "Arabic") or (self.dialect == "Kurmanji" and self.script == "Latin"):
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
        if not isinstance(word, str):
            raise TypeError("Not supported yet.")
        elif (self.dialect == "Sorani" and self.script == "Arabic") or (self.dialect == "Kurmanji" and self.script == "Latin"):
            if self.check_spelling(word):
                return (True, [])
            return (False, list(self.huns.suggest(word)))

    def analyze(self, word_form):
        """
        Morphological analysis of a given word.
        
        It returns morphological analyses. The morphological analysis is returned as a dictionary as follows:
        
        - "pos": the part-of-speech of the word-form according to [the Universal Dependency tag set](https://universaldependencies.org/u/pos/index.html). The gender for nouns in Kurmanji is also provided after the "noun" tag.
        - "description": is flag
        - "prefixes": anything appearing before the base
        - "suffixes": anything appearing after the base
        - "st": the stem of the word
        - "lem": the lemma of the word
        - "formation": if ds flag is set, its value is assigned to description and the value of formation is set to derivational. Although the majority of our morphological rules cover inflectional forms, it is not accurate to say all of them are inflectional. Therefore, we only set this value to derivational wherever we are sure.
        - "base": `ts` flag. The definition of terminal suffix is a bit tricky in Hunspell. According to [the Hunspell documentation](http://manpages.ubuntu.com/manpages/trusty/en/man4/hunspell.4.html), "Terminal suffix fields are inflectional suffix fields "removed" by additional (not terminal) suffixes". In other words, the ts flag in Hunspell represents whatever is left after stripping all affixes. Therefore, it is the morphological base.

        As for the word "دیتبامن" (that I have seen them), the morphological analysis would look like this: [{'pos': ['verb'], 'description': 'past_stem_transitive_active', 'stem': 'دی', 'lemma': ['دیتن'], 'base': 'دیت', 'prefixes': '', 'suffixes': 'بامن'}]
        If the input cannot be analyzed morphologically, an empty list is returned.

        More details regarding Sorani Kurdish morphological analysis can be found at [https://github.com/sinaahmadi/KurdishHunspell](https://github.com/sinaahmadi/KurdishHunspell).

        Nota bene:
        In the previous versions of KLPT, the `stem` module for Kurmanji was relied on the [Apertium project](https://github.com/apertium/apertium-kmr). Now, that is fully replaced by the Kurmanji implementation of [Kurdish Hunspell](https://github.com/sinaahmadi/KurdishHunspell). 

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
            # Given the morphological analysis of a word-form with Hunspell flags, extract relevant information and return a dictionary
            # print(self.huns.analyze(word_form))
            for analysis in list(self.huns.analyze(word_form)):
                analysis_dict = dict()
                for item in analysis.split():
                    if ":" not in item:
                        continue
                    if item.split(":")[1] == "ts":
                        # ts flag exceptionally appears after the value as value:key in the Hunspell output
                        # anything except the terminal_suffix (ts) is considered to be the base
                        analysis_dict["base"] = item.split(":")[0]
                        affixes = utility.extract_prefix_suffix(word_form, item.split(":")[0])
                        analysis_dict["prefixes"] = affixes[0]
                        analysis_dict["suffixes"] = affixes[2]
                        
                    elif item.split(":")[0] in self.hunspell_flags.keys():
                        # assign the key:value pairs from the Hunspell string output to the dictionary output of the current function
                        if item.split(":")[0] == "ds":
                            # for ds flag, add derivation as the formation type, otherwise inflection
                            analysis_dict[self.hunspell_flags[item.split(":")[0]]] = "derivational"
                            analysis_dict[self.hunspell_flags["is"]] = item.split(":")[1]

                        elif item.split(":")[0] == "st":
                            # for st flag, stem should be cleaned first
                            analysis_dict[self.hunspell_flags[item.split(":")[0]]] = self.clean_stem(item.split(":")[1])

                        else:
                            # remove I, T or V using clean_stem()
                            analysis_dict[self.hunspell_flags[item.split(":")[0]]] = self.clean_stem(item.split(":")[1])
                            
                # convert lemma and pos to a list and split based on _ when there is more than one output, e.g. more than one lemma for a given word
                if "lemma" in analysis_dict:
                    analysis_dict["lemma"] = analysis_dict["lemma"].split("_")
                else:
                    analysis_dict["lemma"] = [""]
                
                if "pos" in analysis_dict:
                    analysis_dict["pos"] = analysis_dict["pos"].split("_")
                else:
                    analysis_dict["pos"] = [""]
                
                # for nouns, base is lemma
                if len(analysis_dict["pos"]) and analysis_dict["pos"] != ["verb"]:
                    analysis_dict["lemma"] = [analysis_dict["base"]]

                word_analysis.append(analysis_dict)

        return word_analysis