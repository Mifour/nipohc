import pytest

from .internal.algo import eval_RPN


@pytest.mark.parametrize("input_str,expected", [("3 4 +", 7), ("3 4 - 5 +", 4), ("3 4 x 5 6 x +", 42), ("3 4 x 5 +", 17), ("2 3 ^", 8), ("12 6 /", 2)])
def test_eval_rpn(input_str, expected):
	assert eval_RPN(input_str) == expected


@pytest.mark.parametrize("input_str", ["3 1 2", "", "2 1", "1 + +", "1 + 1"])
def test_raise(input_str):
	with pytest.raises(ValueError):
		eval_RPN(input_str)


def zero_div(input_str):
	with pytest.raises(ZeroDivisionError):
		eval_RPN("1 0 /")
