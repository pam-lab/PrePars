import re


class Normalizer:

    def characterRefine(self, text):

        character_refinement_patterns = [
            (r' {2,}', ' '),  # remove extra spaces
        				(r'\n{3,}', '\n\n'),  # remove extra newlines
            (r'\u200c{2,}', '\u200c'),  # remove extra ZWNJs
        				(r'[ـ\r]', ''),  # remove keshide, carriage returns
            ('"([^\n"]+)"', r'«\1»'),  # replace quotation with gyoome
        				('([\d+])\.([\d+])', r'\1٫\2'),  # replace dot with momayez
        				(r' ?\.\.\.', ' …'),  # replace 3 dots
           	# remove FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA, SHADDA, SUKUN
           	('[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652]', ''),
        ]

        translation_src, translation_dst = ' ىكي“”', ' یکی""'
        translation_src += '0123456789%,'
        translation_dst += '۰۱۲۳۴۵۶۷۸۹٪،'
        translations = self.makeTrans(translation_src, translation_dst)
        character_refinement_patterns = self.compile_patterns(
            character_refinement_patterns)

        text = text.translate(translations)

        for pattern, repl in character_refinement_patterns:
            text = pattern.sub(repl, text)

        return text

    def punctuationRefine(self, text):

        punc_after, punc_before = r'\.:!،؛؟»\]\)\}', r'«\[\(\{'
        punctuation_spacing_patterns = self.compile_patterns([
            # remove space before and after quotation
            ('" ([^\n"]+) "', r'"\1"'),
            (' ([' + punc_after + '])', r'\1'),  # remove space before
            ('([' + punc_before + ']) ', r'\1'),  # remove space after
            # put space after . and :
            ('([' + punc_after[:3] + '])([^ ' + \
             punc_after + '\d۰۱۲۳۴۵۶۷۸۹])', r'\1 \2'),
            ('([' + punc_after[3:] + '])([^ ' + punc_after + '])',
             r'\1 \2'),  # put space after
            ('([^ ' + punc_before + '])([' + punc_before + '])',
             r'\1 \2'),  # put space before
        ])

        for pattern, repl in punctuation_spacing_patterns:
            text = pattern.sub(repl, text)
        return text

    def compile_patterns(self, patterns):
        return [(re.compile(pattern), repl) for pattern, repl in patterns]

    def makeTrans(self, A, B): return dict((ord(a), b) for a, b in zip(A, B))
