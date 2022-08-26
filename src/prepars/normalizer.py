from .regexer import Regexer


class Normalizer:
    def __init__(self) -> None:
        self.regexer = Regexer()

  
    def characterRefine(self, text:str) -> str: 
        """
        This method does some common text preprocessing rules.

        This method is used to:
                *   Remove Extra spaces 
                *   Remove extra newlines
                *   Remove Extra ZWNJs
                *   Remove keshide, carriage
                *   Translate Latin numbers to Persian numbers
                *   Replace quotation with gyoome
                *   Relace dot with momayez
                *   Replace 3 dots
                *   Remove FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA, SHADDA, SUKUN
                
        Args:
            text (str): a pure text to refine
        
        Returns:
            str: Refined text as string
        """
        character_refinement_patterns = [
            (r" {2,}", " "),  # remove extra spaces
            (r"\n{3,}", "\n\n"),  # remove extra newlines
            (r"\u200c{2,}", "\u200c"),  # remove extra ZWNJs
            (r"[ـ\r]", ""),  # remove keshide, carriage returns
            ('"([^\n"]+)"', r"«\1»"),  # replace quotation with gyoome
            ("([\d+])\.([\d+])", r"\1٫\2"),  # replace dot with momayez
            (r" ?\.\.\.", " …"),  # replace 3 dots
            # remove FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA, SHADDA, SUKUN
            ("[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652]", ""),
        ]

        character_refinement_patterns = self.regexer.compilePatterns(
            character_refinement_patterns
        )

        translation_src, translation_dst = " ىكي“”", ' یکی""'
        translation_src += "0123456789%,"
        translation_dst += "۰۱۲۳۴۵۶۷۸۹٪،"
        translations = self.makeTrans(translation_src, translation_dst)
        text = text.translate(translations)

        for pattern, repl in character_refinement_patterns:
            text = pattern.sub(repl, text)

        return text


    def punctuationRefine(self, text):
        """
        This method is responsible to:
            *   Remove space before and after quotation
            *   Remove space before and after symbols
            *   Put space after . and :
        
        Args:
            text (str): a pure text to refine
        Returns:
            text (str): refined text as string
        """
        punc_after, punc_before = r"\.:!،؛؟»\]\)\}", r"«\[\(\{"
        punctuation_spacing_patterns = self.regexer.compilePatterns(
            [
                # remove space before and after quotation
                ('" ([^\n"]+) "', r'"\1"'),
                (" ([" + punc_after + "])", r"\1"),  # remove space before
                ("([" + punc_before + "]) ", r"\1"),  # remove space after
                # put space after . and :
                (
                    "([" + punc_after[:3] + "])([^ " + punc_after + "\d۰۱۲۳۴۵۶۷۸۹])",
                    r"\1 \2",
                ),
                (
                    "([" + punc_after[3:] + "])([^ " + punc_after + "])",
                    r"\1 \2",
                ),  # put space after
                (
                    "([^ " + punc_before + "])([" + punc_before + "])",
                    r"\1 \2",
                ),  # put space before
                ("(?<=.)\s+(?=[\(\{\[])", ""),  # remove space before open symbols
                ("(\)|\}|\]) ?", "\\1 "),  # put space after close symbols
            ]
        )

        for pattern, repl in punctuation_spacing_patterns:
            text = pattern.sub(repl, text)
        return text

    def makeTrans(self, A, B):
        """
        This method is responsible to map chars to each other(zip). example: 1->۱

        Args:
            A (str): source string
            B (str): destination string
        Returns:
            str:  a dictionary of mapped words
        """
        return dict((ord(a), b) for a, b in zip(A, B))

   

    def normalize(self, text):
        """
        This method used to manage normalization operation

        Args:
            text (str): unnormalized text
        Returns:
            str: normalized text
        """
        # Refine chars in text(persianify numbers, remove e-erabs, etc.)
        text = self.characterRefine(text)
        # punctuation refinement
        text = self.punctuationRefine(text)
        return text
