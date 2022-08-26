import json
import re
from pathlib import Path

from .normalizer import Normalizer
from .regexer import Regexer
from .verb import verbProcessing

"""
    This class is responsible to impose compiled rules on text(suffix and prefix)
"""


ROOT = Path(__file__).parents[0]


class Spacing:
    def __init__(self) -> None:
        self.regexer = Regexer()

    

    def suffixFixer(self, text):
        """
        This method applies suffix rules on text

        Args:
            text: a pure text
        Returns:
            processed text
        """
        patterns = self.regexer.sffixPatternGenerator()
        for pat, rep in patterns:
            text = pat.sub(rep, text)
        return text


    def prefixFixer(self, text):
        """
        This method applies prefix rules on text

        Args:
            text:  a pure text
        Returns:
            processed text
        """
        patterns = self.regexer.prefixPatternGenerator()
        for pat, rep in patterns:
            text = pat.sub(rep, text)
        return text

   

    def unregularWords(self, text):
        """
        This method applies unregular words rules on text

        Args:
            text: a pure text
        Returns:
            processed text
        """
        file = open(ROOT / "PVC/Data/TXT/replacement.json", encoding="utf-8")
        rep = json.load(file)

        rep = dict((k, v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)

        return text

    

    def fix(self, text):
        """
        This method used to fix text(call all spacing methods)

        Args:
            text: a pure text
        Returns:
            processed text
        """
        # normalizing the text
        norm = Normalizer()
        text = norm.normalize(text)

        # fix unregular Words
        text = self.unregularWords(text)
        # fix the Verbs
        verb = verbProcessing()
        text = verb.fixVerbs(text)

        # fix the suffixes
        text = self.suffixFixer(text)

        # fix the prefixes
        text = self.prefixFixer(text)

        return norm.normalize(text)
