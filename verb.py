import re
from dataclasses import replace
from pathlib import Path

text = """
می‌رفت
می‌خورد
میرفت
نمیرفت
داشتندمیرفتند
میآجیدم
داشتیممیخوردیم
داشتیم می خوردیم
داشتیمیخوردی
داشتند 
آراسته است
آراسته ام
آراسته ای
آراستهاست
داشتهاست میآراستهاست
"""

HALF_SPACE = '\u200c'
SPACE = ' '
SPACE_OR_HALF = f"[{SPACE}{HALF_SPACE}]"
WORD_BOUNDARY = f"[{SPACE}\W{HALF_SPACE}]"

def to_file(value):
    with open('output.txt', 'a+') as f: 
        f.write(str(value)+'\n')

all_verbs = Path.read_text(
    Path.cwd() / 'PVC/Data/TXT/all_verbs.txt').split('\n')

def remove_half_space(text):
    return text.replace(HALF_SPACE, ' ')

def add_extra_space(text):
    return text.replace('\n', ' \n ').replace('\t', ' \t ') \
    .replace('.', ' . ').replace(',', ' , ').replace('  ',' ')

def remove_double_space(text):
    return text.replace('  ', ' ')

text = remove_half_space(text)
text = add_extra_space(text)

# داشته ام می آراسته ام
text=re.sub(f'{SPACE}(داشته){SPACE_OR_HALF}(اید|ایم|اند|ای|است|ام)',r' \1'+HALF_SPACE+r'\2 ',text)
result = re.sub(f'{SPACE_OR_HALF}?(بودیم|بودند|بودید|بودم|بودی|بود){SPACE_OR_HALF}?',r" \1 ", text)
text = remove_double_space(text)


for verb in all_verbs:

    without_space = verb.replace(" ","")

    # todo: fix آ کلاه دار

    # without_half_space = verb.replace(HALF_SPACE,"")
    # without_both = without_space.replace(HALF_SPACE,"")

    # todo: Maybe half_space check is not necessary. Should consult with Mahdi
    # contains = f' {verb} ' in text \
    #     or f'{HALF_SPACE}{verb} ' in text \
    #     or f' {verb}{HALF_SPACE}' in text \
    #     or f'{HALF_SPACE}{verb}{HALF_SPACE}' in text \
    #     or f' {without_space} ' in text \
    #     or f' {without_half_space} ' in text \
    #     or f' {without_both} ' in text 
    
    contains = f' {verb} ' in text \
        or f' {without_space} ' in text 
    
    if not contains:
        continue

    # this will match all verbs even if there is no space between characters
    fixed_verb = verb.replace(SPACE, f"{SPACE_OR_HALF}?")

    regex = f"{WORD_BOUNDARY}({fixed_verb}){WORD_BOUNDARY}"
    for item in re.finditer(regex, text):
        start, end = item.start(),item.end()
        if text[start] == HALF_SPACE:
            text = text[:start] + SPACE + text[start+1:]
        if text[end-1] == HALF_SPACE:
            text = text[:end-1] + SPACE + text[end:]
        
        result=re.sub(f'{SPACE_OR_HALF}?(نمی|می){SPACE_OR_HALF}?(.+)',
            r" \1"+HALF_SPACE+r"\2", text[start:end])
        text = text[:start] + result + text[end:]
        text = remove_double_space(text)

        result = re.sub(f'{SPACE_OR_HALF}?(داشت)(یم|ید|ند|م|ی)?{SPACE_OR_HALF}?(.+)',
            r" \1\2 \3", text[start:end])
        text = text[:start] + result + text[end:]
        text = remove_double_space(text)

        # may have bugs because of ? in regex
        result = re.sub(f'{SPACE_OR_HALF}?(اید|ایم|اند|ام|ای|است){SPACE_OR_HALF}',
            HALF_SPACE+r"\1 ", text[start:end])
        text = text[:start] + result + text[end:]
        text = remove_double_space(text)

        result = re.sub(f'{SPACE_OR_HALF}?(بودیم|بودند|بودید|بودم|بودی|بود){SPACE_OR_HALF}?',
            r" \1 ", text[start:end])
        text = text[:start] + result + text[end:]
        text = remove_double_space(text)



to_file(str(text))
