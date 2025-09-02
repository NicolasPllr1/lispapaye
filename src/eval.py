from .parser import (
    OPERATORS_TOKEN_KIND,
    Atom,
    Expression,
    Operator,
)
from .token import LispValue, Token, TokenKind


def evaluate(expresssion: Expression) -> LispValue:
    match expresssion:
        case Atom(atom):
            return atom.literal
        case Operator():
            raise NotImplementedError("Value of an operator not implemented yet")
        case sub_expr:
            op = sub_expr[0]
            assert isinstance(op, Operator), (
                f"First item of a list should be an operator, got: {op}"
            )

            if op.op.kind == TokenKind.QUOTE:
                assert len(sub_expr) == 2, (
                    f"Invalid arguments for quote operator. Should be a single argument, got {len(sub_expr) - 1}: {sub_expr[1:]}"
                )
                return sub_expr[1]  # NOTE: by pass evaluation of the args
            else:
                raw_args = sub_expr[1:]  # expressions
                args_values = [evaluate(arg) for arg in raw_args]

                return evalate_single_op(op.op, args_values)


def evalate_single_op(op: Token, args: list[LispValue]) -> LispValue | list[LispValue]:
    assert op.kind in OPERATORS_TOKEN_KIND, (
        f"operator {op} does not have the expected kind. Should be one of: {OPERATORS_TOKEN_KIND}"
    )
    match op.kind:
        case TokenKind.PLUS:
            assert all([isinstance(arg, int | float) for arg in args]), (
                f"Invalid arguments. Addition operator operates on number, received: {args}"
            )
            return sum([float(arg) for arg in args])
        case TokenKind.MINUS:
            assert all([isinstance(arg, int | float) for arg in args]), (
                f"Invalid arguments. Substraction operator operates on number, received: {args}"
            )
            res = args[0]
            for term in args[1:]:
                res -= term
            return res
        case TokenKind.SLASH:
            assert all([isinstance(arg, int | float) for arg in args]), (
                f"Invalid arguments. Division operator operates on number, received: {args}"
            )
            res = args[0]
            for divisor in args[1:]:
                if divisor == 0:
                    raise ValueError(
                        f"Invalid argument. Divisor should not be 0: {divisor}"
                    )
                res /= divisor
            return res
        case TokenKind.CONS:
            assert len(args) == 2, (
                f"Invalid number of arguments to cons operator, should be two but got {len(args)}: {args}"
            )
            return args
