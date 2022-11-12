from lexer import get_next_token
from tokens import MBNF_Token, MBNF_TokenType
from syntax_tree import AST, NodeType


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

    root.children.append(definition(token_generator))


def definition(token_generator):
    root = AST()
    current_token = next(token_generator)

    root.children.push(AST(node_type=NodeType.VALUE, value=current_token))

    current_token = next(token_generator)

    match current_token.dict():
        case MBNF_Token(
            token_type=MBNF_TokenType.NONTERMINAL, value=value
        ) | MBNF_Token(token_type=MBNF_TokenType.NONTERMINAL, value=value) as terminal:
            root.node_type = NodeType.CONCATENATION
            root.children.append(AST(node_type=NodeType.VALUE, value=terminal))
        case MBNF_Token(token_type=MBNF_TokenType.END_OF_EXPR, value=value) as token:
            return root


def mult_node():
    pass


def singleton_node():
    pass
