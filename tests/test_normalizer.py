from curses import halfdelay
from prepars.normalizer import Normalizer
import pytest

HALF_SPACE = "\u200c"


@pytest.mark.parametrize(
    "input, expected",
    [
        ("\n\n\n","\n\n"),
        ("  "," "),
        ("   "," "),
        (HALF_SPACE+HALF_SPACE,HALF_SPACE),
        ("1234567890","۱۲۳۴۵۶۷۸۹۰"),
        ("123.123","۱۲۳٫۱۲۳"),
        ("مهدي","مهدی"),
        ("مردك","مردک"),
        ("مْحٌمْدٌْاْمٌیٍر","محمدامیر"),
    ],
)
def test_characterRefine(input, expected):
    assert Normalizer().characterRefine(input) == expected
    assert Normalizer().normalize(input) == expected


