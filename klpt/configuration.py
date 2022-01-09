#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Configuration class of the Kurdish Language Processing Toolkit (KLPT).

Raises:
    ValueError: Unknown dialect
    ValueError: Unknown script
    ValueError: Unknown numeral

Returns:
    obj: an object to be passed to other packages
"""
import sys
sys.path.append('../klpt')
import json
import klpt

class Configuration:
    def __init__(self, config_dict):#dialect, script, numeral="Latin", target_script=None, unknown="�"):
        """

        Args:
            dialect (str): the name of the dialect or its ISO 639-3 code
            script (str): the name of the script
            numeral (str): the type of the numeral

        """

        with open(klpt.get_data("data/default-options.json"), encoding = "utf-8") as options_file:
            self.options = json.load(options_file)
        
        self.unknown = None

        if "script" in config_dict:
            self.validate_script(config_dict["script"])
        else:
            self.script = None

        if "dialect" in config_dict:
            self.validate_dialect(config_dict["dialect"])
        else:
            self.dialect = None

        if "numeral" in config_dict:
            self.validate_numeral(config_dict["numeral"])
        else:
            self.numeral = None
    
        if "target_script" in config_dict:
            self.validate_target_script(config_dict["target_script"])
        else:
            self.target_script = None

        if "unknown" in config_dict:
            self.validate_unknown(config_dict["unknown"])
        else:
            self.user_UNKNOWN = "�"

    def normalize_arguments(self, argument):
        return argument.lower().capitalize()

    def validate_script(self, script):
        if self.normalize_arguments(script) not in self.options["scripts"]:
            raise ValueError(f'Unknown script. Available options: {self.options["scripts"]}')
        else:
            self.script = self.normalize_arguments(script)

    def validate_dialect(self, dialect):
        if self.normalize_arguments(dialect) in self.options["dialects"]:
            self.dialect = self.normalize_arguments(dialect)
        elif self.normalize_arguments(dialect) in list(self.options["dialects"].values()):
            self.dialect = dict(zip(self.options["dialects"].values(), self.options["dialects"].keys()))[self.normalize_arguments(dialect)]
        else:
            raise ValueError(f'Unknown dialect. Available options: {self.options["dialects"]}')

    def validate_numeral(self, numeral):
        if self.normalize_arguments(numeral) not in self.options["numerals"]:
            raise ValueError(f'Unknown numeral. Available options: {self.options["numerals"]}')
        else:
            self.numeral = self.normalize_arguments(numeral).lower().capitalize()

    def validate_target_script(self, target_script):
        # complete it; if source and target scripts are identical, then return the input without processing
        if target_script == "Latin":
            self.target_script = self.normalize_arguments(target_script)
            self.mode = "arabic_to_latin"
        elif target_script == "Arabic":
            self.target_script = self.normalize_arguments(target_script)
            self.mode = "latin_to_arabic"
        else:
            raise ValueError(f'Unknown transliteration option. Available options: {self.options["transliterator"]}')

    def validate_unknown(self, unknown):
        if len(unknown):
            self.user_UNKNOWN = unknown
        else:
            raise ValueError(f'Unknown unknown tag. Select a non-empty token (e.g. <UNK>.')


# To Do:
# User should be able to update the configuration at any point in such a way that the class that uses that instance also get updated