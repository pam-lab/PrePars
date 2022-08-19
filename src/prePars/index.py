from pathlib import Path
from spacing import Spacing


def to_file(value):
    with open('output.txt', 'a+', encoding="utf-8") as f:
        f.write(str(value)+'\n')


log_file = Path('output.txt')
if log_file.exists():
    log_file.unlink()

text = "سلام من مهدی آخی هستم(مَهدی)و این اولین تست ما در این نرم افزار است.\
من می خواهم بگویم که سیاست گذاری ما درست نیست\
 ما بی هیچ علاقه‌ای ، برای این شهر جنگ خواهیم کرد .\
همهٔ ما میدانیم که این درست نیست ."

# refine all
sp = Spacing()
output = sp.fix(text)

to_file(output)
