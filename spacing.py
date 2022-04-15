from pathlib import Path
import json
import re

from verb import verbProcessing
from regexer import Regexer
from normalizer import Normalizer

class Spacing:
    def __init__(self) -> None:
        self.regexer = Regexer()

    def suffixFixer(self, text):

        patterns = self.regexer.sffixPatternGenerator()
        for pat, rep in patterns:
            text = pat.sub(rep, text)      
        return text

    def prefixFixer(self, text):

        patterns = self.regexer.prefixPatternGenerator()
        for pat, rep in patterns:
            text = pat.sub(rep, text)      
        return text

    def unregularWords(self, text):
        
        file = open(Path.cwd()/'PVC/Data/TXT/replacement.json', encoding="utf-8")
        rep = json.load(file)

        rep = dict((k, v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)

        return text

    def fix(self, text):

        # normalizing the text
        norm = Normalizer()
        text = norm.normalize(text)

        # fix the Verbs
        verb=verbProcessing()
        text = verb.fixVerbs(text)

        # fix the suffixes
        text = self.suffixFixer(text)

        # fix the prefixes
        text = self.prefixFixer(text)

        # fix unregular Words
        text = self.unregularWords(text)

        return norm.normalize(text)
