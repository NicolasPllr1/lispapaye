from dataclasses import dataclass
from enum import Enum


class TokenKind(Enum):
    PLUS = "+"
    MINUS = "-"
    SLASH = "/"
    #
    QUOTE = "quote"
    QUOTE_ABR = "'"
    CONS = "cons"
    #
    NIL = "nil"
    TRUE = "t"
    #
    STRING = None
    #
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"


@dataclass
class Token:
    kind: TokenKind
    lexeme: str  # from the source
    literal: str | None  # not every token is a literal / has a literal _value_


def main():
    print("Hello from lisp-interpreter!")


if __name__ == "__main__":
    main()
