#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The tokenization module of the Kurdish Language Processing Toolkit (KLPT)
    Based on the Kurdish Tokenization project: https://github.com/sinaahmadi/KurdishTokenization

    
    Regarding multi-word expressions, we assume that each part of a compound form is separated with a dash (-). Therefore, hyphens are not considered a punctuation mark in the tokenization process.

    * 2020/07/23 20:01:05
    * Sina Ahmadi

"""
import json
import sys
import re
sys.path.append('../klpt')
from klpt.configuration import Configuration
from klpt.preprocess import Preprocess
import klpt

class Tokenize:
    """

    This module focuses on the tokenization of both Kurmanji and Sorani dialects of Kurdish with the following functions:

    - `word_tokenize`: tokenization of texts into tokens (both [multi-word expressions](https://aclweb.org/aclwiki/Multiword_Expressions) and single-word tokens).
    - `mwe_tokenize`: tokenization of texts by only taking compound forms into account
    - `sent_tokenize`: tokenization of texts into sentences

    The module is based on the [Kurdish tokenization project](https://github.com/sinaahmadi/KurdishTokenization).

    Example:
    
    ```python
    >>> from klpt.tokenize import Tokenize

    >>> tokenizer = Tokenize("Kurmanji", "Latin")
    >>> tokenizer.word_tokenize("ji bo fortê xwe avêtin")
    ['▁ji▁', 'bo', '▁▁fortê‒xwe‒avêtin▁▁']
    >>> tokenizer.mwe_tokenize("bi serokê hukûmeta herêma Kurdistanê Prof. Salih re saz kir.")
    'bi serokê hukûmeta herêma Kurdistanê Prof . Salih re saz kir .'

    >>> tokenizer_ckb = Tokenize("Sorani", "Arabic")
    >>> tokenizer_ckb.word_tokenize("بە هەموو هەمووانەوە ڕێک کەوتن")
    ['▁بە▁', '▁هەموو▁', 'هەمووانەوە', '▁▁ڕێک‒کەوتن▁▁']
    ```

    """
    def __init__(self, dialect, script, numeral="Latin", separator='▁'):

        # validate parameters
        with open(klpt.get_data("data/tokenize.json"), encoding = "utf-8") as tokenize_file:
            self.tokenize_map = json.load(tokenize_file)

        with open(klpt.get_data("data/preprocess_map.json"), encoding = "utf-8") as preprocess_file:
            self.preprocess_map = json.load(preprocess_file)

        # sentence tokenizer variables
        self.dialect, self.script = dialect, script
        self.alphabets = "([%s])"%"".join(self.tokenize_map["sent_tokenize"][self.dialect][self.script]["alphabet"])
        self.prefixes = self.tokenize_map["sent_tokenize"][self.dialect][self.script]["prefixes"]
        self.suffixes = self.tokenize_map["sent_tokenize"][self.dialect][self.script]["suffixes"]
        self.starters = self.tokenize_map["sent_tokenize"][self.dialect][self.script]["starters"]
        self.websites = self.tokenize_map["sent_tokenize"]["universal"]["websites"]
        self.acronyms = self.tokenize_map["sent_tokenize"][self.dialect][self.script]["acronyms"]
        self.digits = "([%s])"%"".join(list(set(list(self.preprocess_map["normalizer"]["universal"]["numerals"][numeral].values()))))

        # load lexicons
        with open(klpt.data_directory["tokenize"][self.dialect][self.script], "r", encoding = "utf-8") as f_lexicon:
            self.lexicon = json.load(f_lexicon)["Lexicon"]
         
        self.mwe_lexicon = {lemma: form for lemma, form in self.lexicon.items() if "-" in lemma}

        with open(klpt.data_directory["morphemes"][self.dialect], "r", encoding = "utf-8") as f_morphemes:
            self.morphemes = json.load(f_morphemes)["Morphemes"]["Concatenated"][self.script]
        
    
    def mwe_tokenize(self, sentence, separator="▁▁", in_separator="‒", punct_marked=False, keep_form=False):
        """
        Multi-word expression tokenization

        Args:
            sentence (str): sentence to be split by multi-word expressions
            separator (str): a specific token to specify a multi-word expression. By default two ▁ (▁▁) are used for this purpose.
            in_separator (str): a specific token to specify the composing parts of a multi-word expression. By default a dash - is used for this purpose.
            keep_form (boolean): if set to True, the original form of the multi-word expression is returned the same way provided in the input. On the other hand, if set to False, the lemma form is used where the parts are delimited by a dash ‒, as in "dab‒û‒nerît"

        Returns:
            str: sentence containing d multi-word expressions using the separator

        """
        sentence = " " + sentence + " "

        if not punct_marked:
            # find punctuation marks and add a space around
            for punct in self.tokenize_map["word_tokenize"][self.dialect][self.script]["punctuation"]:
                if punct in sentence:
                    sentence = sentence.replace(punct, " " + punct + " ")

        # look for compound words and delimit them by double separator
        for compound_lemma in self.mwe_lexicon:
            compound_lemma_context = " " + compound_lemma + " "
            if compound_lemma_context in sentence:
                if keep_form:
                    sentence = sentence.replace(compound_lemma_context, " ▁▁" + compound_lemma + "▁▁ ")
                else:
                    sentence = sentence.replace(compound_lemma_context, " ▁▁" + compound_lemma.replace("-", in_separator) + "▁▁ ")                    

            # check the possible word forms available for each compound lemma in the lex files, too
            # Note: compound forms don't have any hyphen or separator in the lex files
            for compound_form in self.mwe_lexicon[compound_lemma]["token_forms"]:
                compound_form_context = " " + compound_form + " "
                if compound_form_context in sentence:
                    if keep_form:
                        sentence = sentence.replace(compound_form_context, " ▁▁" + compound_form + "▁▁ ")
                    else:
                        sentence = sentence.replace(compound_form_context, " ▁▁" + compound_lemma.replace("-", in_separator) + "▁▁ ")
                        

        # print(sentence)
        return sentence.replace("  ", " ").replace("▁▁", separator).strip()
        

    def word_tokenize(self, sentence, separator="▁", mwe_separator="▁▁", keep_form=False):
        """Word tokenizer

        Args:
            sentence (str): sentence or text to be tokenized

        Returns:
            [list]: [a list of words]
       
        """
        # find multi-word expressions in the sentence
        sentence = self.mwe_tokenize(sentence, keep_form=keep_form)

        # find punctuation marks and add a space around
        for punct in self.tokenize_map["word_tokenize"][self.dialect][self.script]["punctuation"]:
            if punct in sentence:
                sentence = sentence.replace(punct, " " + punct + " ")

        # print(sentence)
        tokens = list()
        # split the sentence by space and look for identifiable tokens
        for word in sentence.strip().split():
            if "▁▁" in word:
                # the word is previously detected as a compound word
                tokens.append(word)
            else:
                if word in self.lexicon:
                    # check if the word exists in the lexicon
                    tokens.append("▁" + word + "▁")
                else:
                    # the word is neither a lemma nor a compound
                    # morphological analysis by identifying affixes and clitics
                    token_identified = False

                    for preposition in self.morphemes["prefixes"]:
                        if word.startswith(preposition) and len(word.split(preposition, 1)) > 1:
                            if word.split(preposition, 1)[1] in self.lexicon:
                                word = "▁".join(["", self.morphemes["prefixes"][preposition], word.split(preposition, 1)[1], ""])
                                token_identified = True
                                break
                            elif self.mwe_tokenize(word.split(preposition, 1)[1], keep_form=keep_form) != word.split(preposition, 1)[1]:
                                word = "▁" + self.morphemes["prefixes"][preposition] + self.mwe_tokenize(word.split(preposition, 1)[1], keep_form=keep_form)
                                token_identified = True
                                break
                    
                    if not token_identified:
                        for postposition in self.morphemes["suffixes"]:
                            if word.endswith(postposition) and len(word.rpartition(postposition)[0]):
                                if word.rpartition(postposition)[0] in self.lexicon:
                                    word = "▁" + word.rpartition(postposition)[0] + "▁" + self.morphemes["suffixes"][postposition]
                                    break
                                elif self.mwe_tokenize(word.rpartition(postposition)[0], keep_form=keep_form) != word.rpartition(postposition)[0]:
                                    word = ("▁" + self.mwe_tokenize(word.rpartition(postposition)[0], keep_form=keep_form) + "▁" + self.morphemes["suffixes"][postposition] + "▁").replace("▁▁▁", "▁▁")
                                    break
            
                    tokens.append(word)
        # print(tokens)
        return " ".join(tokens).replace("▁▁", mwe_separator).replace("▁", separator).split()


    def sent_tokenize(self, text):
        """Sentence tokenizer

        Args:
            text ([str]): [input text to be tokenized by sentences]

        Returns:
            [list]: [a list of sentences]

        """
        text = " " + text + "  "
        text = text.replace("\n", " ")
        text = re.sub(self.prefixes, "\\1<prd>", text)
        text = re.sub(self.websites, "<prd>\\1", text)
        text = re.sub("\s" + self.alphabets + "[.] ", " \\1<prd> ", text)
        text = re.sub(self.acronyms + " " + self.starters, "\\1<stop> \\2", text)
        text = re.sub(self.alphabets + "[.]" + self.alphabets + "[.]" + self.alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
        text = re.sub(self.alphabets + "[.]" + self.alphabets + "[.]", "\\1<prd>\\2<prd>", text)
        text = re.sub(" " + self.suffixes + "[.] " + self.starters, " \\1<stop> \\2", text)
        text = re.sub(" " + self.suffixes + "[.]", " \\1<prd>", text)
        text = re.sub(self.digits + "[.]" + self.digits, "\\1<prd>\\2", text)
        
        # for punct in self.tokenize_map[self.dialect][self.script]["compound_puncts"]:
        #     if punct in text:
        #         text = text.replace("." + punct, punct + ".")
        
        for punct in self.tokenize_map["sent_tokenize"][self.dialect][self.script]["punct_boundary"]:
            text = text.replace(punct, punct + "<stop>")
        
        text = text.replace("<prd>", ".")
        sentences = text.split("<stop>")
        sentences = [s.strip() for s in sentences if len(s.strip())]
        
        return sentences