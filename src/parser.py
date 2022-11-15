import json
from typing import Generator

from lexer import get_next_token
from syntax_tree import AST, NodeType
from tokens import MBNF_TokenType, get_closing_token


class UnexpectedTokenException(Exception):
    def __init__(self, token):
        self.message = f"Unexpected token {token}"


class Parser:
    def __init__(self, token_generator: Generator):
        self.token_generator = token_generator
        self.current_token = next(token_generator)

    def eat(self, token_type: MBNF_TokenType):
        if self.current_token.token_type != token_type:
            raise UnexpectedTokenException(self.current_token)
        self.current_token = next(self.token_generator)

    def expr_generator(self):
        while self.current_token.token_type != MBNF_TokenType.END_OF_EXPR:
            yield self.term()

    def definition(self):
        root = AST(node_type=NodeType.ASSIGN)
        root.children.append(self.factor())

        self.eat(MBNF_TokenType.OP_ASSIGN)

        root.children = [node for node in self.expr_generator()]

        return root

    def expr(self):
        match self.current_token.token_type:
            case MBNF_TokenType.TERMINAL | MBNF_TokenType.NONTERMINAL:
                return self.term()
            case MBNF_TokenType.OPTION_OPEN | MBNF_TokenType.GROUP_OPEN | MBNF_TokenType.DUPLICATION_OPEN:
                return self.grouping()
            case MBNF_TokenType.END_OF_EXPR:
                return None
            case _:
                raise UnexpectedTokenException(self.current_token)

    def grouping(self):
        root = AST()
        terminating_op = get_closing_token(self.current_token.token_type)
        if not terminating_op:
            raise UnexpectedTokenException(self.current_token)

        self.eat(self.current_token.token_type)

        root.children.append(self.expr())

        self.eat(terminating_op)
        return root

    def term(self):
        root = AST()
        root.children.append(self.factor())
        print("TERM-0", self.current_token)

        if self.current_token.token_type == MBNF_TokenType.OP_ALTERNATIVE:
            self.node_type = NodeType.ALTERNATIVE
            self.eat(self.current_token.token_type)
        elif (
            self.current_token.token_type == MBNF_TokenType.TERMINAL
            or self.current_token.token_type == MBNF_TokenType.NONTERMINAL
        ):
            root.node_type = NodeType.CONCATENATION
        root.children.append(self.factor())
        print("TERM", self.current_token)
        return root

    def factor(self):
        if (
            self.current_token.token_type == MBNF_TokenType.NONTERMINAL
            or self.current_token.token_type == MBNF_TokenType.TERMINAL
        ):
            node = AST(node_type=NodeType.VALUE, value=self.current_token)
            self.eat(token_type=self.current_token.token_type)
            return node

        return self.expr()


if __name__ == "__main__":
    parser = Parser(get_next_token())

    print(json.dumps(json.loads(parser.definition().json()), indent=4))
