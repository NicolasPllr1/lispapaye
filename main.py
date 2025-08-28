import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from rich import print


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
    STRING = "string"
    NUMBER = "number"
    #
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    #
    SYMBOL = "symbol"  # e.g. in 'Artichoke, Artichoke is the symbol (~variable name ?)


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
            case ")":
                tok_kind = TokenKind.RIGHT_PAREN
                lexeme = source[idx]
            case number if number.isdigit():
                tok_kind = TokenKind.NUMBER

                # NOTE: for now, assume its an integer, not a float (i.e. no decimal point)
                head = idx
                # look for the end of the number
                while idx + 1 < len(source) and source[idx + 1].isdigit():
                    idx += 1
                lexeme = source[head : idx + 1]  # TODO: double check the bounds
                literal = str(int(lexeme))  # NOTE: assuming int again
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

                while (
                    idx < len(source) and source[idx] != '"' and source[idx].isalpha()
                ):
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
                if (
                    idx + len(TokenKind.NIL.value) - 1 < len(source)
                    and source[idx : idx + len(TokenKind.NIL.value)]
                    == TokenKind.NIL.value
                ):
                    tok_kind = TokenKind.NIL
                    lexeme = TokenKind.NIL.value
                    literal = None
                    idx += len(TokenKind.NIL.value)
                elif (
                    idx + len(TokenKind.CONS.value) - 1 < len(source)
                    and source[idx : idx + len(TokenKind.CONS.value)]
                    == TokenKind.CONS.value
                ):
                    tok_kind = TokenKind.CONS
                    lexeme = TokenKind.CONS.value
                    literal = None
                    idx += len(TokenKind.CONS.value)
                elif (
                    idx + len(TokenKind.QUOTE.value) - 1 < len(source)
                    and source[idx : idx + len(TokenKind.QUOTE.value)]
                    == TokenKind.QUOTE.value
                ):
                    tok_kind = TokenKind.QUOTE
                    lexeme = TokenKind.QUOTE.value
                    literal = None
                    idx += len(TokenKind.QUOTE.value)
                else:
                    # try to parse a symbol
                    tok_kind = TokenKind.SYMBOL
                    head = idx  # idx of the double-quote " symbol

                    while idx < len(source) and source[idx].isalpha():
                        idx += 1

                    if head < idx:
                        lexeme = source[head:idx]
                    else:
                        raise ValueError(
                            f"Expected variable name to have at least length of 1 at index {idx}: {source[idx]}"
                        )

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


# Kind of tokens which can be used as a _function argument_
OPERATORS_TOKEN_KIND: set[TokenKind] = {
    TokenKind.PLUS,
    TokenKind.MINUS,
    TokenKind.SLASH,
    #
    TokenKind.QUOTE,
    TokenKind.CONS,
}

SPECIAL_OPERATORS_TOKEN_KIND: set[TokenKind] = {
    TokenKind.QUOTE_ABR,
}


@dataclass
class Operator:
    op: Token  # token-kind in OPERATORS_TOKEN_KIND


# Kind of tokens which are atomic piece of _data_
ATOM_TOKEN_KINDS: set[TokenKind] = {
    TokenKind.STRING,
    TokenKind.NUMBER,
    #
    TokenKind.NIL,
    TokenKind.TRUE,
    #
    TokenKind.SYMBOL,
}


@dataclass
class Atom:
    """
    Special leaf tokens. Like elementary pieces of data such as a literal string or a number.
    """

    atom: Token  # token-kind in ATOM_TOKEN_KINDS


# "All Lisp expressions are either atoms, like 1, or lists, which consist of zero or more expressions enclosed in parentheses" from Graham's book, chap 2.
# either an atom, an operator (i.e. a function or a special operator) or a list of them
Expression = Atom | Operator | list["Expression"]

PAREN_TOKEN_KINDS = {TokenKind.LEFT_PAREN, TokenKind.RIGHT_PAREN}
assert (
    ATOM_TOKEN_KINDS
    | OPERATORS_TOKEN_KIND
    | SPECIAL_OPERATORS_TOKEN_KIND
    | PAREN_TOKEN_KINDS
    == set(TokenKind)
), "Not all token-kinds covered by parsing sets"


@dataclass
class Parser:
    tokens: list[Token]
    idx: int = 0  # idx of the token currently being processed

    def parse(self) -> Expression:
        "Assume the tokens reprends a single expression (no declarations, pure? lisp!)"

        if self.idx >= len(self.tokens):
            raise ValueError("Ran out of tokens")

        tok = self.tokens[self.idx]
        self.idx += 1  # 'consume' the tok

        if tok.kind in ATOM_TOKEN_KINDS:
            return Atom(atom=tok)
        elif tok.kind in OPERATORS_TOKEN_KIND:
            return Operator(op=tok)
        elif tok.kind in SPECIAL_OPERATORS_TOKEN_KIND:
            # NOTE: assuming they all work like the abbreviated quote. We only support this one in the scanner anyway for now
            assert tok.kind == TokenKind.QUOTE_ABR, (
                "special operator is expected to be the abbreviated quote for now"
            )

            # "You can get the effect of calling quote by affixing a ' to the front of any expression" from Graham's book
            quoted_ast = self.parse()

            # re-wrap using the normal quote
            # My idea is that the quote abbreviation is syntactic sugar for (quote ...) --> we recover the full ast for the user
            return [
                Operator(op=Token(kind=TokenKind.QUOTE, lexeme="quote", literal=None)),
                quoted_ast,
            ]

        elif tok.kind == TokenKind.LEFT_PAREN:
            list_items: list[Expression] = []
            while (
                self.idx < len(self.tokens)
                and self.tokens[self.idx].kind != TokenKind.RIGHT_PAREN
            ):
                next_item = self.parse()
                list_items.append(next_item)

            # check if we stopped parsing because we run out of tokens
            ran_out_of_tokens = self.idx == len(self.tokens)
            if ran_out_of_tokens:
                raise ValueError(
                    "Ran out of tokens before finding the end of the list (right paren)"
                )

            # consume the right paren
            self.idx += 1
            return list_items

        else:
            raise ValueError(
                f"Unexpected token at idx {self.idx}: {tok}. "
                "Expected either an atom of data, an operator or a left parenthesis"
            )


def process_snippet(snippet_name: str, snippet_dir: Path):
    print(f"--- {snippet_name} ---")
    raw_source_text = (snippet_dir / snippet_name).read_text()
    print(f"Source:\n{raw_source_text}")

    # try to scan the source!
    tokens = scan(raw_source_text)

    ast = Parser(tokens=tokens).parse()
    print(f"Final AST for {snippet_name}:")
    print(ast)


def main():
    LISP_SNIPPET_DIR = Path("lisp_snippets")

    if len(sys.argv) > 1:
        snippet_name = sys.argv[1]
        process_snippet(snippet_name, LISP_SNIPPET_DIR)
    else:
        for snippet_path in LISP_SNIPPET_DIR.glob("*.lisp"):
            process_snippet(snippet_path.name, LISP_SNIPPET_DIR)


if __name__ == "__main__":
    main()
