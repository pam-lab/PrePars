from prepars import normalizer
import pytest

@pytest.mark.parametrize("input, expected", [("  ", " "),])
def remote_extra_spaces(input, expected):
    assert normalizer().characterRefine(input) == expected

def test_always_fail():
    assert False