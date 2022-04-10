import re
from dataclasses import replace
from pathlib import Path

text = """
ویکی‌پدیای فارسی نام یکی از دانشنامه‌های فارسی‌زبان در اینترنت و یکی از نسخه‌های ویکی‌پدیا، از پروژه‌های بنیاد ویکی‌مدیا است . میرفت می‌رفت می رفت ویکی‌پدیا پروژهٔ بزرگی است که هدف آن ساخت دانشنامه‌هایی با محتوای آزاد با مشارکت همگان و به همهٔ زبان‌های ممکن است.
این دانشنامهٔ فارسی ۱۸ سال پیش (دقیقاً در ۲۸ آذر ۱۳۸۲ / ۱۹ دسامبر ۲۰۰۳) فعالیت خود را آغاز کرد و حجم آن در حدود یک‌سالگی به ۱۰۰۰ مقاله، در دوسالگی (بهمن ۱۳۸۴) -با داشتن رتبهٔ سی‌وهشتم در میان ویکی‌پدیاها- به ۱۰هزار مقاله، و در هفت‌سالگی (شهریور ۱۳۸۹) به ۱۰۰هزار نوشتار رسید . ویکی‌پدیای فارسی هم‌اکنون (۱۰ فروردین ۱۴۰۱ خورشیدی برابر با ۳۰ مارس ۲۰۲۲ میلادی) ۸۹۲٬۶۳۹ نوشتار دارد.[۳]
در اسفند ۱۳۹۹ (مارس ۲۰۲۱) ویکی‌پدیای فارسی با ۱٬۱۰۷٬۵۵۰ کاربرِ ثبت‌نام‌کرده، در ردهٔ شانزدهم ویکی‌پدیاها، از لحاظ شمار کاربرانِ فعال در ردهٔ یازدهم و از جهت شمار مدیران (۳۷ مدیر) در ردهٔ هجدهم جای دارد .[۳] ویکی‌پدیای فارسی تا پایان فوریه ۲۰۲۱، دارای ۴۱۰ مقاله خوب و ۱۹۲ مقاله برگزیده است.
 می‌نوشتم و کار انجام میدادم در این حین‌می‌کرد کار انجام شود‌و خوب انجام شود 
می‌رفت
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

text = remove_half_space(text)


for verb in all_verbs:

    without_space = verb.replace(" ","")
    without_half_space = verb.replace(HALF_SPACE,"")
    without_both = without_space.replace(HALF_SPACE,"")

    # todo: Maybe half_space check is not necessary. Should consult with Mahdi
    contains = f' {verb} ' in text \
        or f'{HALF_SPACE}{verb} ' in text \
        or f' {verb}{HALF_SPACE}' in text \
        or f'{HALF_SPACE}{verb}{HALF_SPACE}' in text \
        or f' {without_space} ' in text \
        or f' {without_half_space} ' in text \
        or f' {without_both} ' in text 

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


        
to_file(str(text))
