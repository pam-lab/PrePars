import re
import csv
from pathlib import Path


HALF_SPACE = '‌'

class Regexer:

    def __init__(self, regexPath='PVC/Data/TXT/suffix.csv') -> None:
        file = open(Path.cwd()/regexPath, encoding="utf-8")
        self.rules = csv.reader(file)
    
    def compilePatterns(self, patterns):
        return [(re.compile(pattern), repl) for pattern, repl in patterns]

    def patternGenerator(self):
        patterns = []
        for item in self.rules:
            space = '' if item[1] == 'a' else HALF_SPACE
            # if item[2]!='':
            #     pattern = r'('+item[2]+r')'+r'( )'+'('+item[0]+')'+r'( )'
            #     replacement = space+r'\2\3'
            # else:
            pattern = r'( )'+'('+item[0]+')'+r'( )'
            replacement = space+r'\2\3'
            patterns.append((re.compile(pattern), replacement))
        
        return self.compilePatterns(patterns)
