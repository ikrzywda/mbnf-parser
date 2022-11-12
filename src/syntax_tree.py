from enum import Enum
from typing import List

from tokens import MBNF_Token


class NodeType(Enum):
    ALTERNATIVE = 0
    OPTION = 1
    ASSIGN = 2
    GROUP = 3
    COPY = 4
    MBNF_Token = 5


class AST:
    def __init__(
        self,
        node_type: NodeType,
        value: List["AST"] | List[MBNF_Token] | "AST" | MBNF_Token,
    ):
        self.node_type = node_type
        self.value = value
