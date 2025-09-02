from dataclasses import dataclass

from .token import Token, TokenKind


# my current mental model for operators are that they are symbols which refer to functions
@dataclass
class Operator:
    op: Token  # token-kind should be in OPERATORS_TOKEN_KIND or SPECIAL_OPERATORS_TOKEN_KIND ('quote')


# Kind of tokens which are atomic piece of _data_, or a symbol
# My current mental model for symbols is that they are either built-in 'keywords'/functions or akin to variable names
ATOM_TOKEN_KINDS: set[TokenKind] = {
    TokenKind.STRING,
    TokenKind.NUMBER,
    #
    TokenKind.NIL,
    TokenKind.TRUE,
    #
    TokenKind.SYMBOL,
}


OPERATORS_TOKEN_KIND: set[TokenKind] = {
    TokenKind.PLUS,
    TokenKind.MINUS,
    TokenKind.SLASH,
    #
    TokenKind.QUOTE,
    TokenKind.CONS,
}

# special functions, which do not follow the typical (operator, arg1, ..., argN) pattern
SPECIAL_OPERATORS_TOKEN_KIND: set[TokenKind] = {
    TokenKind.QUOTE_ABR,
}


@dataclass
class Atom:
    """
    Special leaf tokens. Like elementary pieces of data such as a literal string or a number.
    """

    atom: Token  # token-kind should be in ATOM_TOKEN_KINDS


# "Another beauty of Lisp notation is: this is all there is.  All Lisp expressions are either atoms, like 1, or lists, which consist of zero or more expressions enclosed in parentheses." from Graham's book (end of 2.1)
# The wikipedia page is also helpful: https://en.wikipedia.org/wiki/Lisp_(programming_language)#Syntax_and_semantics
# --> An expression is either an atom, an operator (i.e. a function or a special operator) or a list of them
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

            # "You can get the effect of calling quote by affixing a ' to the front of any expression" from Graham's book (end of 2.2)
            quoted_ast = self.parse()

            # re-wrap using the normal quote (i.e., desugar the expression)
            # My idea is that the quote abbreviation is syntactic sugar for (quote ...) --> we recover the full ast for the user , i.e. prepent the quote
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
