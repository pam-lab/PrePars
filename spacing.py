from regexer import Regexer

class Spacing:
    def __init__(self) -> None:
        self.regexer = Regexer()

    def suffixFixer(self, text):

        patterns = self.regexer.patternGenerator()
        for pat, rep in patterns:
            text = pat.sub(rep, text)      
        return text
