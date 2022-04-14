import re
import csv
from pathlib import Path


HALF_SPACE = '‌'

class Regexer:

    def __init__(self) -> None:

        file = open(Path.cwd()/'PVC/Data/TXT/suffix.csv', encoding="utf-8")
        self.suffix = csv.reader(file)

        file = open(Path.cwd()/'PVC/Data/TXT/prefix.txt', encoding="utf-8")
        self.prefix = csv.reader(file)

    def compilePatterns(self, patterns):
        return [(re.compile(pattern), repl) for pattern, repl in patterns]



    def sffixPatternGenerator(self):
        patterns = []
        for item in self.suffix:
            space = '' if item[1] == 'a' else HALF_SPACE
            if item[2]!='':
                pattern = r'(?<=('+item[2]+'))\s+(?=('+item[0]+'))'
                replacement = '‌' if item[1] == 'a' else ''
                patterns.append(tuple([re.compile(pattern), replacement]))

            pattern = r'( )'+'('+item[0]+')'+r'( )'
            replacement = space+r'\2\3'
            patterns.append(tuple([re.compile(pattern), replacement]))
        
        return patterns

    def prefixPatternGenerator(self):
        patterns = []
        for item in self.prefix:
            space = '' if item[1] == 'a' else HALF_SPACE
            if item[2] != '':
                pattern = '(?<=('+item[0]+'))\s+(?=('+item[2]+'))'
                replacement = '‌' if item[1] == 'a' else ''
                patterns.append(tuple([re.compile(pattern), replacement]))

            pattern = r'( )'+'('+item[0]+')'+r'( )'
            replacement = r'\1\2'+ space
            patterns.append(tuple([re.compile(pattern), replacement]))

        return patterns
