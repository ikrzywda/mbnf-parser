from enum import Enum
from pydantic import BaseModel

SINGLETON_TOKEN_SET = "[]{}()|=,."


class MBNF_TokenType(str, Enum):
    OPTION_OPEN = "["
    OPTION_CLOSE = "]"
    DUPLICATION_OPEN = "{"
    DUPLICATION_CLOSE = "}"
    GROUP_OPEN = "("
    GROUP_CLOSE = ")"

    OP_ALTERNATIVE = "|"
    OP_ASSIGN = "="

    QUOTE = '"'
    SEPARATOR = ","
    END_OF_EXPR = "."

    NONTERMINAL = "NONTERMINAL"
    TERMINAL = "TERMINAL"


class MBNF_Token(BaseModel):
    token_type: MBNF_TokenType
    value: str
