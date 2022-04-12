from dataclasses import replace
import re
from pathlib import Path

samples = """
میخورد
می رفت
میرفت
نمیرفت
داشتندمیرفتند
میآجیدم
داشتیممیخوردیم
داشتیمیخوردی
آراسته است
نمیرفتهاست
نرفتهاند
آراستهاست
داشتهاست میآراستهاست
نمیآراسته بوده ام
می آزرده بوده اند
خواهمخورد

رفت می رفت داشتم می رفتم
داشتممیرفتم
"""

HALF_SPACE = '\u200c'
SPACE = ' '
SPACE_OR_HALF = f'[{HALF_SPACE}{SPACE}]*'
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

        # text = self.remove_half_space(text)
        # text = self.add_extra_space(text)

        # text = re.sub(f' (داشته) ?(اید|ایم|اند|ای|است|ام)',r' \1'+HALF_SPACE+r'\2 ',text)
        # text = re.sub(f' (بوده)(ایم|اید|اند|ای|است|ام)',r" \1"+HALF_SPACE+r"\2 ", text)
        # text = re.sub(f' (بودیم|بودند|بودید|بودم|بودی|بود) ',r" \1 ", text)
        # text = re.sub(f' (باشم|باشد|باشیم|باشید|باشند|باشی) ',r" \1 ", text)
        # text = re.sub(f' (داریم|دارند|دارید|داری|دارد|دارم) ?',r" \1 ", text)
        # text = re.sub(f' (داشتند|داشتید|داشتیم|داشتم|داشتی|داشت) ',r" \1 ", text)
        # text = re.sub(f' (ن)?(خواهم|خواهی|خواهد|خواهیم|خواهید|خواهند) ?',r" \1\2 ", text)
        text = self.remove_double_space(text)

        for item in all_verbs:
            
            if not item:
                continue

            verb, tag1, tag2, tag3 = item.split(',')

            # todo: fix آ کلاه دار
            contains = verb.replace(" ","") in text.replace(" ","").replace(HALF_SPACE,"")

            if not contains:
                continue

            # this will match all verbs even if there is no space between characters
            fixed_verb = verb.replace(' ', f" *").replace(HALF_SPACE,f'{HALF_SPACE}*')

            regex = f"{WORD_BOUNDARY}({fixed_verb}){WORD_BOUNDARY}"
            for item in re.finditer(regex, text):
                start, end = item.start(),item.end()

                # if text[start] == HALF_SPACE:
                #     text = text[:start] + SPACE + text[start+1:]
                # if text[end-1] == HALF_SPACE:
                #     text = text[:end-1] + SPACE + text[end:]
                
                # result=re.sub(f'{SPACE}?(نمی|می){SPACE}?',
                #     r" \1"+HALF_SPACE, text[start:end])
                # text = self.apply_regex_result(text, start, end, result)

                # result = re.sub(f' +(اید|ایم|اند|ام|ای|است)', HALF_SPACE+r"\1", text[start:end])
                # text = self.apply_regex_result(text, start, end, result)
                result = text[start:end]

                if tag1 == 'PAST' and tag2 =='INDICATIVE':
                    # آزردم آزردی آزرد 
                    if tag3 == 'SIMPLE':
                        continue
                    # می آزردم
                    if tag3 == 'IMPERFECTIVE':
                        result=re.sub(f'(نمی|می){SPACE_OR_HALF}(\w+)', r'\1'+HALF_SPACE+r'\2', text[start:end])

                    if tag3 == 'PROGRESSIVE':
                        result=re.sub(f'(داشت)(یم|ید|ند|ی|م)?{SPACE_OR_HALF}(نمی|می){SPACE_OR_HALF}(\w+)', r'\1\2 \3'+HALF_SPACE+r'\4', text[start:end])
                
                    if tag3 == 'NARRATIVE':
                        result = re.sub(f'(\w+){SPACE_OR_HALF}(ایم|اید|اند|ام|ای|است)', r'\1'+HALF_SPACE+r'\2', text[start:end])

                    if tag3 == 'NARRATIVE_IMPERFECTIVE':
                        result = re.sub(f'(نمی|می)(\w+)(ایم|اید|اند|ام|ای|است)', r'\1'+HALF_SPACE+r'\2'+HALF_SPACE+r'\3', text[start:end])
                        


                text = text[:start] + result + text[end:]

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
