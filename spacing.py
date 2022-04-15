from regexer import Regexer
import re
from pathlib import Path
import json

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
        # print(rep)

        rep = dict((k, v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)

        return text
