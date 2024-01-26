import operator

from enum import Enum
from functools import reduce
from typing import Callable


def parse_operator(c: str, do_not_raise: bool) -> Callable[[int | float, int | float], int | float]:
	match c:
		case "+":
			return operator.add
		case "-":
			return operator.sub
		case "x" | "*":
			return operator.mul
		case "/":
			return operator.truediv
		case "//":
			return operator.floordiv
		case "%":
			return operator.modulo
		case "@":
			return operator.matmul
		case "**" | "^":
			return operator.pow
		case _:
			if do_not_raise:
				return None
			raise ValueError(f"unrecognized operator {c}")


def parse_int_or_float(x: str) -> int | float:
	# may throw a ValueError
	f = float(x)
	if f % 1.0:
		# fractional part is not zero
		return f
	return int(f)


def atomic_polish_operation(a: int | float, b: int | float, c: Callable) -> int | float:
	#op = parse_operator(c)
	return c(parse_int_or_float(a), parse_int_or_float(b))

def eval_RPN(input_str: str) -> int | float:
	# Reverse polish Notation evaluator
	stack = input_str.split()
	if len(stack) < 3:
		raise ValueError(f"invalid input: {input_str}")
	while stack:
		for i in range(2, len(stack)):
			if c := parse_operator(stack[i], do_not_raise=True):
				a, b, _ = stack.pop(i - 2), stack.pop(i - 2), stack.pop(i - 2)
				break
		else:
			raise ValueError(f"did not found any operator {' '.join(stack)}")
		res = atomic_polish_operation(a, b, c)
		if not stack:
			break
		stack.insert(0, res)
	return res


