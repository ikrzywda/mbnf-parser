from enum import Enum
from typing import List

from tokens import MBNF_Token
from pydantic import BaseModel


class NodeType(Enum):
    ALTERNATIVE = 0
    OPTION = 1
    ASSIGN = 2
    GROUP = 3
    COPY = 4
    VALUE = 5
    CONCATENATION = 6


class AST(BaseModel):
    node_type: NodeType
    value: MBNF_Token
    children: List["AST"]
