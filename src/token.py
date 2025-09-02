from dataclasses import dataclass
from enum import Enum


class TokenKind(Enum):
    PLUS = "+"
    MINUS = "-"
    SLASH = "/"
    #
    # TODO: add other 'basic' built-ins: list, car/cdr, first, lambda
    QUOTE = "quote"
    QUOTE_ABR = "'"
    CONS = "cons"
    #
    NIL = "nil"
    TRUE = "t"
    #
    STRING = "string"
    NUMBER = "number"
    #
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    #
    SYMBOL = "symbol"  # e.g. in 'Artichoke, Artichoke is the symbol (~variable name ?)


LispValue = str | int | float | bool | None


@dataclass
class Token:
    kind: TokenKind
    lexeme: str  # from the source
    literal: LispValue  # not every token is a literal / has a literal _value_
