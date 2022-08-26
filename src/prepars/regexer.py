import csv
import re
from pathlib import Path

"""
    This class used to manage rules and regex 
"""

HALF_SPACE = "‌"

ROOT = Path(__file__).parents[0]


class Regexer:
    def __init__(self) -> None:

        file = open(ROOT / "PVC/Data/TXT/suffix.csv", encoding="utf-8")
        self.suffix = csv.reader(file)

        file = open(ROOT / "PVC/Data/TXT/prefix.txt", encoding="utf-8")
        self.prefix = csv.reader(file)

    

    def compilePatterns(self, patterns):
        """
        This method take an array of tuples (pattern, replacement) and compile them
        
        Args:
            patterns: array of tuples (pattern, replacement)
        
        Returns:
            an array of compiled regex patterns
        """
        return [(re.compile(pattern), repl) for pattern, repl in patterns]


    def sffixPatternGenerator(self):
        """
        This method fetchs all suffix pattern from rule file and generate regex patterns

        Args:
            self: python class
        Returns: 
            an array of regex patterns[(pattern, replacement)]
        """
        patterns = []
        for item in self.suffix:
            # specify which space should be used. h: half space, a: affix
            space = "" if item[1] == "a" else HALF_SPACE
            # check if rule has exception
            if item[2] != "":
                pattern = r"(?<=(" + item[2] + "))\s+(?=(" + item[0] + "))"
                replacement = "‌" if item[1] == "a" else ""
                patterns.append(tuple([re.compile(pattern), replacement]))

            pattern = r"( )" + "(" + item[0] + ")" + r"( )"
            replacement = space + r"\2\3"
            patterns.append(tuple([re.compile(pattern), replacement]))

        return patterns

   

    def prefixPatternGenerator(self):
        """
        This method fetchs all affix pattern from rule file and generate regex patterns

        Args: 
            self: python class
        Returns: 
            an array of regex patterns[(pattern, replacement)]
        """
        patterns = []
        for item in self.prefix:
            # specify which space should be used. h: half space, a: affix
            space = "" if item[1] == "a" else HALF_SPACE
            # check if rule has exception
            if item[2] != "":
                pattern = "(?<=(" + item[0] + "))\s+(?=(" + item[2] + "))"
                replacement = HALF_SPACE if item[1] == "a" else ""
                patterns.append(tuple([re.compile(pattern), replacement]))

            pattern = r"( )" + "(" + item[0] + ")" + r"( )"
            replacement = r"\1\2" + space
            patterns.append(tuple([re.compile(pattern), replacement]))

        return patterns
