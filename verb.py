from dataclasses import replace
import re
from pathlib import Path

samples = """
می‌ رفت
میخورد
میرفت
نمیرفت
داشتندمیرفتند
میآجیدم
داشتیممیخوردیم
داشتیمیخوردی
آراسته است
آراسته ام
آراسته ای
آراستهاست
داشتهاست میآراستهاست
نمیآراسته بوده ام
می آزرده بوده اند
خواهمخورد
"""

HALF_SPACE = '\u200c'
SPACE = ' '
WORD_BOUNDARY = f"[{SPACE}\W{HALF_SPACE}]"    

class Verb_Processing:
        
    def __init__(self) -> None:
        pass

    def remove_half_space(self,text):
        return text.replace(HALF_SPACE, ' ')

    def add_extra_space(self, text) -> str:
        return text.replace('\n', ' \n ').replace('\t', ' \t ') \
        .replace('.', ' . ').replace(',', ' , ').replace('  ',' ')

    def remove_double_space(self, text) -> str:
        return text.replace('  ', ' ')

    def fix_verb_half_space(self, text):

        all_verbs = Path.read_text(Path.cwd() / 'PVC/Data/TXT/all_verbs.txt').split('\n')
        
        text = self.remove_half_space(text)
        text = self.add_extra_space(text)

        text = re.sub(f' (داشته) ?(اید|ایم|اند|ای|است|ام)',r' \1'+HALF_SPACE+r'\2 ',text)
        text = re.sub(f' (بوده)(ایم|اید|اند|ای|است|ام)',r" \1"+HALF_SPACE+r"\2 ", text)
        text = re.sub(f' (بودیم|بودند|بودید|بودم|بودی|بود) ',r" \1 ", text)
        text = re.sub(f' (باشم|باشد|باشیم|باشید|باشند|باشی) ',r" \1 ", text)
        text = re.sub(f' (داریم|دارند|دارید|داری|دارد|دارم) ?',r" \1 ", text)
        text = re.sub(f' (داشتند|داشتید|داشتیم|داشتم|داشتی|داشت) ',r" \1 ", text)
        text = re.sub(f' (ن)?(خواهم|خواهی|خواهد|خواهیم|خواهید|خواهند) ?',r" \1\2 ", text)
        text = self.remove_double_space(text)

        for verb in all_verbs:


            without_space = verb.replace(" ","")
            # todo: fix آ کلاه دار
            
            contains = f' {verb} ' in text \
                or f' {without_space} ' in text \
                or f' {without_space} ' in text.replace(" ","")
            
            if not contains:
                continue

            
            # this will match all verbs even if there is no space between characters
            fixed_verb = verb.replace(SPACE, f"{SPACE}?")

            to_file(str(verb))
            regex = f"{WORD_BOUNDARY}({fixed_verb}){WORD_BOUNDARY}"
            for item in re.finditer(regex, text):
                start, end = item.start(),item.end()
                if text[start] == HALF_SPACE:
                    text = text[:start] + SPACE + text[start+1:]
                if text[end-1] == HALF_SPACE:
                    text = text[:end-1] + SPACE + text[end:]
                
                result=re.sub(f'{SPACE}?(نمی|می){SPACE}?',
                    r" \1"+HALF_SPACE, text[start:end])
                text = self.apply_regex_result(text, start, end, result)

                result = re.sub(f'{SPACE}(داشت)(یم|ید|ند|م|ی)?{SPACE}',
                    r" \1\2 ", text[start:end])
                text = self.apply_regex_result(text, start, end, result)

                # may have bugs because of ? in regex
                result = re.sub(f' (اید|ایم|اند|ام|ای|است)', HALF_SPACE+r"\1 ", text[start:end])
                text = self.apply_regex_result(text, start, end, result)

                result = re.sub(f'{SPACE}(بودیم|بودند|بودید|بودم|بودی|بود){SPACE}',r" \1 ", text[start:end])
                text = self.apply_regex_result(text, start, end, result)

        return text

    def set_result(self, text, start, end, result):
            text = text[:start] + result + text[end:]
            return text

    def apply_regex_result(self, text, start, end, result):
        text = self.set_result(text, start, end, result)
        text = self.remove_double_space(text)
        return text

def to_file(value):
    with open('output.txt', 'a+') as f: 
        f.write(str(value)+'\n')

log_file = Path('output.txt')
if log_file.exists():
    log_file.unlink()

verb_processing=Verb_Processing()
samples_answers=verb_processing.fix_verb_half_space(samples)
to_file(samples_answers)
