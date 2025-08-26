from pathlib import Path
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
    NUMBER = None
    #
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"


@dataclass
class Token:
    kind: TokenKind
    lexeme: str  # from the source
    literal: str | None  # not every token is a literal / has a literal _value_


def scan(source: str, debug: bool = False) -> list[Token]:
    "From raw source text to a 'stream' of tokens"
    source = source.strip()

    tokens: list[Token] = []
    idx = 0  # idx into the source text

    while idx < len(source):
        if debug:
            print(f"Scanning at idx {idx}: {source[idx]}")
        tok_kind: TokenKind
        literal: str | None = None
        lexeme: str
        match source[idx]:
            case " ":
                # skip whitespace
                if debug:
                    print("skipping whitespace")
                idx += 1
                continue
            case "(":
                tok_kind = TokenKind.LEFT_PAREN
                lexeme = source[idx]
            case "(":
                tok_kind = TokenKind.RIGHT_PAREN
                lexeme = source[idx]
            case number if number.isdigit():
                tok_kind = TokenKind.NUMBER

                # NOTE: for now, assume its an integer, not a float (i.e. no decimal point)
                head = idx
                # look for the end of the number
                idx += 1
                while idx < len(source) and source[idx].isdigit():
                    idx += 1
                lexeme = source[head:idx]  # TODO: double check the bounds
                if debug:
                    print(f"after number scanning, idx is {idx}")
            case '"':
                tok_kind = TokenKind.STRING

                # parse the string. Essentially hunting for the closing " symbol before the end of the source text
                head = idx  # idx of the double-quote " symbol
                idx += 1  # right after the "

                if not idx < len(source):
                    raise ValueError(
                        "Expect a string after a double-quote, found the end of the source file"
                    )

                while idx < len(source) and source[idx] != '"':
                    idx += 1

                # check the closing double-quote " has been found before the end of the file
                if idx == len(source):
                    raise ValueError(
                        f"closing quote not found after quote at index {head}: {source[head:]}",
                    )

                lexeme = source[
                    head : idx + 1
                ]  # double check the bounds. `idx` should be the idx of the closing "
                if idx == head + 1:  # the string was the empty string
                    literal = ""
                else:
                    literal = source[head + 1 : idx]

            case "t":
                tok_kind = TokenKind.TRUE
                lexeme = source[idx]
            case "nil":
                tok_kind = TokenKind.NIL
                lexeme = source[idx]
            case "cons":
                tok_kind = TokenKind.CONS
                lexeme = source[idx]
            case "quote":
                tok_kind = TokenKind.QUOTE
                lexeme = source[idx]
            case "'":
                tok_kind = TokenKind.QUOTE_ABR
                lexeme = source[idx]
            case "/":
                tok_kind = TokenKind.SLASH
                lexeme = source[idx]
            case "+":
                tok_kind = TokenKind.PLUS
                lexeme = source[idx]
            case "-":
                tok_kind = TokenKind.MINUS
                lexeme = source[idx]
            case _:
                raise ValueError(f"Unexpected character at index {idx}: {source[idx]}")

        tok = Token(
            kind=tok_kind,
            lexeme=lexeme,
            literal=literal,
        )
        if debug:
            print("token scanned:\n", tok)

        tokens.append(tok)

        # go to next token
        idx += 1

    return tokens


def main():
    LISP_SNIPPET_DIR = Path("lisp_snippets")
    snippet_name = "addition.lisp"

    raw_source_text = (LISP_SNIPPET_DIR / snippet_name).read_text()
    print(f"source, {len(raw_source_text)=}:\n{raw_source_text}")
    print("length stripped: ", len(raw_source_text.strip()))

    # try to scan the source!
    tokens = scan(raw_source_text, debug=True)

    print("Tokens:\n", tokens)


if __name__ == "__main__":
    main()
