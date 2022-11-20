from parser import Parser
from lexer import get_next_token
from syntax_tree import NodeType, AST
from typing import Dict
from lexer import MBNF_TokenType


class RegexTranslator:
    def __init__(self, input_symbol_table: Dict[str, AST]):
        self.input_symbol_table = input_symbol_table
        self.output_symbol_table: Dict[str, str] = {}

    def translate(self):
        for key, value in self.input_symbol_table.items():
            if self.output_symbol_table.get(key):
                pass
            self.output_symbol_table[key] = self.expression(value.children[0])

    def assign(self, key: str):
        output = self.input_symbol_table[key].children[0]
        self.output_symbol_table[key] = output
        return output

    def expression(self, root: AST):
        match root.node_type:
            case NodeType.ALTERNATIVE:
                return self.alternative(root)
            case NodeType.VALUE:
                return self.value(root)

    def alternative(self, root: AST):
        expr_l = self.expression(root.children[0])
        expr_r = self.expression(root.children[1])
        return f"{expr_l}|{expr_r}"

    def option():
        pass

    def grouping():
        pass

    def copy():
        pass

    def concatenation():
        pass

    def value(self, root: AST):
        token_value = root.value.value
        if root.value.token_type == MBNF_TokenType.TERMINAL:
            return token_value
        if self.output_symbol_table.get(token_value):
            return self.output_symbol_table[token_value]
        output_value = self.expression(self.input_symbol_table[token_value].children[0])
        self.output_symbol_table[token_value] = output_value
        return output_value


if __name__ == "__main__":
    parser = Parser(get_next_token())
    parser.definition()
    # roots = [r for r in parser.definition()]
    translator = RegexTranslator(parser.symbol_table)
    translator.translate()
    print(translator.output_symbol_table)
