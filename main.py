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
    lexeme: str | None  # TODO: think about the need for both lexeme and literal
    literal: str | None


def main():
    print("Hello from lisp-interpreter!")


if __name__ == "__main__":
    main()
