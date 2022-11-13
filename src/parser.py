from lexer import get_next_token
from tokens import MBNF_Token, MBNF_TokenType
from syntax_tree import AST, NodeType
import itertools


def expr(token_generator: get_next_token):
    root = AST()
    current_token = next(token_generator)
    if not current_token and current_token.token_type is not MBNF_TokenType.NONTERMINAL:
        raise Exception("Syntax error: assignment can only be done on nonterminal")
    root.children.append(AST(node_type=NodeType.VALUE, value=current_token))
    current_token = next(token_generator)

    if not current_token and current_token.token_type is not MBNF_TokenType.OP_ASSIGN:
        raise Exception("Syntax error: assignment expression must contain '='")
    root.node_type = NodeType.ASSIGN
    root.value = current_token

    root.children.append(term(token_generator))

    current_token = next(token_generator)
    if not current_token and current_token.token_type is not MBNF_TokenType.END_OF_EXPR:
        raise Exception("Syntax error: expected '.'")

    return root


def term(token_generator: get_next_token):
    current_token = next(token_generator)

    match current_token.token_type:
        case MBNF_TokenType.OPTION_OPEN | MBNF_TokenType.DUPLICATION_OPEN | MBNF_TokenType.GROUP_OPEN:
            return grouping(token_generator, current_token)  # list
        case MBNF_TokenType.NONTERMINAL | MBNF_TokenType.TERMINAL:
            return binop(token_generator)
        case _:
            raise Exception(f"Syntax error: unexpected token {current_token}")


def factor(token_generator: get_next_token):
    current_token = next(token_generator)

    if (
        current_token.token_type == MBNF_TokenType.NONTERMINAL
        or current_token.token_type == MBNF_TokenType.TERMINAL
    ):
        return AST(node_type=NodeType.VALUE, value=current_token)

    raise Exception(f"Syntax error: unexpected token {current_token}")


def binop(token_generator):
    root = AST()

    root.children.append(factor(token_generator))

    current_token = next(token_generator)

    if current_token.token_type == MBNF_TokenType.OP_ALTERNATIVE:
        root.node_type = NodeType.ALTERNATIVE
    elif (
        current_token.token_type == MBNF_TokenType.TERMINAL
        or current_token.token_type == MBNF_TokenType.NONTERMINAL
    ):
        root.node_type = NodeType.CONCATENATION

    root.children.append(term(token_generator))
    return root


def grouping(token_generator, start_token):
    root = AST()
    termination_token_type = None
    current_token = None

    match start_token.token_type:
        case MBNF_TokenType.OPTION_OPEN:
            root.node_type = NodeType.OPTION
            termination_token_type = MBNF_TokenType.OPTION_CLOSE
        case MBNF_TokenType.DUPLICATION_OPEN:
            root.node_type = NodeType.COPY
            termination_token_type = MBNF_TokenType.DUPLICATION_CLOSE
        case MBNF_TokenType.GROUP_OPEN:
            termination_token_type = MBNF_TokenType.GROUP_CLOSE
            root.node_type = NodeType.GROUP

    current_token = next(token_generator)
    while current_token.token_type != termination_token_type:
        itertools.chain([current_token], token_generator)
        root.children.append(term(token_generator))
    return root


if __name__ == "__main__":
    gen = get_next_token()
    print(expr(gen))
