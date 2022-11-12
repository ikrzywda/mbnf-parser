from typing import List
from tokens import MBNF_Token, MBNF_TokenType
import sys
import re


def get_token(in_str: str) -> MBNF_Token:
    token_type: MBNF_TokenType | None = None
    value: str | None = None


class Lexer:
    current_line_MBNF_Tokens: List[str]

    def get_next_MBNF_Token(self):
        if not self.current_line_MBNF_Tokens:
            raw_input = sys.stdin.readline()
            if not raw_input:
                return None
            self.current_line_MBNF_Tokens = raw_input.split(" ")

        return get_token(self.current_line_MBNF_Tokens.pop(0))


def lexer():
    buf = sys.stdin.buffer.read()
    for c in buf:
        if c == 0:
            print("EOF")
        print(c, chr(c))


if __name__ == "__main__":
    lexer()
