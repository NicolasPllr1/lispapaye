from rich import print

from .token import LispValue, Token, TokenKind


def scan(source: str, debug: bool = False) -> list[Token]:
    "From raw source text to a 'stream' of tokens"
    source = source.strip()

    tokens: list[Token] = []
    idx = 0  # idx into the source text

    while idx < len(source):
        if debug:
            print(f"Scanning at idx {idx}: {source[idx]}")
        tok_kind: TokenKind
        literal: LispValue = None
        lexeme: str
        match source[idx]:
            case " " | "\n":
                # skip whitespace
                if debug:
                    print(f"skipping whitespace idx {idx}")
                idx += 1
                continue
            case "(":
                tok_kind = TokenKind.LEFT_PAREN
                lexeme = source[idx]
            case ")":
                tok_kind = TokenKind.RIGHT_PAREN
                lexeme = source[idx]
            case number if number.isdigit():
                # https://www.gnu.org/software/emacs/manual/html_node/elisp/Float-Basics.html
                tok_kind = TokenKind.NUMBER

                head = idx
                no_dot_yet = True  # keep track if we've encountered a '.', e.g. in '3.14', or '3.'

                # look for the end of the number
                while idx + 1 < len(source) and (
                    source[idx + 1].isdigit() or (source[idx + 1] == "." and no_dot_yet)
                ):
                    idx += 1  # update idx: now source[idx] is the digit (or '.') we just checked
                    if source[idx] == ".":
                        no_dot_yet = False  # we just passed a dot

                # NOTE: source[idx] is the last digit (or '.') in the number
                lexeme = source[head : idx + 1]

                if no_dot_yet:
                    literal = int(lexeme)
                elif source[idx] == ".":
                    # no decimal part, like in '3.' -> view it as an int
                    literal = int(lexeme[:-1])
                else:
                    literal = float(lexeme)
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
                if check_longer_token_match(TokenKind.NIL, idx, source):
                    tok_kind = TokenKind.NIL
                    lexeme = TokenKind.NIL.value
                    literal = None
                    idx += len(TokenKind.NIL.value)
                elif check_longer_token_match(TokenKind.CONS, idx, source):
                    tok_kind = TokenKind.CONS
                    lexeme = TokenKind.CONS.value
                    literal = None
                    idx += len(TokenKind.CONS.value)
                elif check_longer_token_match(TokenKind.QUOTE, idx, source):
                    tok_kind = TokenKind.QUOTE
                    lexeme = TokenKind.QUOTE.value
                    literal = None
                    idx += len(TokenKind.QUOTE.value)
                else:
                    if debug:
                        print("parsing a symbol")
                    # try to parse a symbol
                    tok_kind = TokenKind.SYMBOL
                    head = idx  # idx of the symbol first character

                    while idx < len(source) and source[idx].isalpha():
                        idx += 1

                    if head < idx:
                        lexeme = source[head:idx]
                        literal = lexeme

                        idx -= 1
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
            print("token scanned:", tok)

        tokens.append(tok)

        # go to next token
        idx += 1

    return tokens


def check_longer_token_match(
    target_token_kind: TokenKind, idx: int, source: str
) -> bool:
    return (
        idx + len(target_token_kind.value) - 1 < len(source)
        and source[idx : idx + len(target_token_kind.value)] == target_token_kind.value
    )
