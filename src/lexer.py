import sys
from tokens import MBNF_TokenType, SINGLETON_TOKEN_SET, MBNF_Token


def getc():
    buffer = sys.stdin.buffer.read()
    for c in buffer:
        yield chr(c)


def get_string_token(it):
    token_buffer = ""

    for c in it:
        if not c.isalnum():
            break
        token_buffer += c
    return token_buffer


def get_next_token():
    gc = getc()
    for c in gc:
        if c in SINGLETON_TOKEN_SET:
            yield MBNF_Token(token_type=MBNF_TokenType(c), value=c)
        elif c == '"':
            yield MBNF_Token(
                token_type=MBNF_TokenType.TERMINAL, value=get_string_token(gc)
            )
        elif c.isalnum():
            value = c + get_string_token(gc)
            yield MBNF_Token(
                token_type=MBNF_TokenType.NONTERMINAL,
                value=value,
            )
        elif not c:
            raise Exception("Syntax error")


if __name__ == "__main__":
    for tok in get_next_token():
        print(tok)
