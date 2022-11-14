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


def get_closing_token(value: MBNF_TokenType) -> MBNF_TokenType | None:
    match value:
        case MBNF_TokenType.OPTION_OPEN:
            return MBNF_TokenType.OPTION_CLOSE
        case MBNF_TokenType.DUPLICATION_OPEN:
            return MBNF_TokenType.DUPLICATION_CLOSE
        case MBNF_TokenType.GROUP_OPEN:
            return MBNF_TokenType.GROUP_CLOSE
        case _:
            return None


class MBNF_Token(BaseModel):
    token_type: MBNF_TokenType
    value: str
