import re
from dataclasses import replace
from pathlib import Path

text = """
ویکی‌پدیای فارسی نام یکی از دانشنامه‌های فارسی‌زبان در اینترنت و یکی از نسخه‌های ویکی‌پدیا، از پروژه‌های بنیاد ویکی‌مدیا است . میرفت می‌رفت می رفت ویکی‌پدیا پروژهٔ بزرگی است که هدف آن ساخت دانشنامه‌هایی با محتوای آزاد با مشارکت همگان و به همهٔ زبان‌های ممکن است.
این دانشنامهٔ فارسی ۱۸ سال پیش (دقیقاً در ۲۸ آذر ۱۳۸۲ / ۱۹ دسامبر ۲۰۰۳) فعالیت خود را آغاز کرد و حجم آن در حدود یک‌سالگی به ۱۰۰۰ مقاله، در دوسالگی (بهمن ۱۳۸۴) -با داشتن رتبهٔ سی‌وهشتم در میان ویکی‌پدیاها- به ۱۰هزار مقاله، و در هفت‌سالگی (شهریور ۱۳۸۹) به ۱۰۰هزار نوشتار رسید . ویکی‌پدیای فارسی هم‌اکنون (۱۰ فروردین ۱۴۰۱ خورشیدی برابر با ۳۰ مارس ۲۰۲۲ میلادی) ۸۹۲٬۶۳۹ نوشتار دارد.[۳]
در اسفند ۱۳۹۹ (مارس ۲۰۲۱) ویکی‌پدیای فارسی با ۱٬۱۰۷٬۵۵۰ کاربرِ ثبت‌نام‌کرده، در ردهٔ شانزدهم ویکی‌پدیاها، از لحاظ شمار کاربرانِ فعال در ردهٔ یازدهم و از جهت شمار مدیران (۳۷ مدیر) در ردهٔ هجدهم جای دارد .[۳] ویکی‌پدیای فارسی تا پایان فوریه ۲۰۲۱، دارای ۴۱۰ مقاله خوب و ۱۹۲ مقاله برگزیده است.
"""

HALF_SPACE = '\u200c'
SPACE = ' '
SPACE_OR_HALF = f"[{SPACE}{HALF_SPACE}]"
WORD_BOUNDARY = f"[{SPACE}\W{HALF_SPACE}]"


def remove_half_space(text):
    return text.replace(HALF_SPACE, ' ')


all_verbs = Path.read_text(
    Path.cwd() / 'PVC/Data/TXT/all_verbs.txt').split('\n')

# text = remove_half_space(text)


for verb in all_verbs:
    contains = f' {verb} ' in text \
        or f'{HALF_SPACE}{verb} ' in text \
        or f' {verb}{HALF_SPACE}' in text \
        or f'{HALF_SPACE}{verb}{HALF_SPACE}' in text \
        or f' {verb.replace(" ","").replace(HALF_SPACE,"")} ' in text

    if not contains:
        continue

    # this will match all verbs even if there is no space between characters
    fixed_verb = verb.replace(' ', f"{SPACE_OR_HALF}*")

    regex = f"{WORD_BOUNDARY}({fixed_verb}){WORD_BOUNDARY}"
    for item in re.finditer(regex, text):
        start, end = item.start(),item.end()
        print(start,end,item)
        
        
