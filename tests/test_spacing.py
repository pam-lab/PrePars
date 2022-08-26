from prepars.spacing import Spacing
import pytest


@pytest.mark.parametrize(
    "input, expected",
    [
        ("طوطی وار", "طوطی‌وار"),
        ("دیوانه وار", "دیوانه‌وار")
    ],
)
def test_suffix(input, expected):
    print(Spacing().suffixFixer(input))
    assert Spacing().suffixFixer(input) == expected


@pytest.mark.parametrize("input, expected", [("", "")])
def test_prefix(input, expected):
    print(Spacing().prefixFixer(input))
    assert Spacing().prefixFixer(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ("اینگونه", "این گونه"),
        ("آن‌گونه", "آن گونه"),
        ("همینطور", "همین طور"),
        ("چه‌سان", "چه سان"),
        ('آن‌گاه', 'آن گاه'),
        ('آنگاه', 'آن گاه')
    ],
)
def test_unregularWords(input, expected):
    assert Spacing().unregularWords(input) == expected
