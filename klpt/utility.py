#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Utility functions used in the the Kurdish Language Processing Toolkit (KLPT).

    * created: 2020/12/07 10:12:06
    * author: Sina Ahmadi

"""

import sys
sys.path.append('../klpt')

def extract_prefix_suffix(word_form, base):
    """Given a substring, find the preceding and succeeding characters as prefix and suffix, respectively

    Args:
        word_form ([str]): [a word]
        base ([str]): [the stem or base of the word]

    Returns:
        [list]: [a list containing three elements in str showing the preceding and succeeding characters before the stem or the base]
    """
    if word_form == base:
        return '', word_form, ''
    elif len(word_form) > len(base):
        for i in range(len(word_form)):
            if word_form[i: i + len(base)] == base:
                return word_form[0: i], base, word_form[i + len(base):]
    
    return '', word_form, ''
