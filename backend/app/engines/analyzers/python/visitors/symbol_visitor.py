import ast


class SymbolVisitor(ast.NodeVisitor):
    def __init__(self):
        self.classes = []
        self.functions = []

    def visit_ClassDef(self, node: ast.ClassDef):
        self.classes.append(
            {
                "name": node.name,
                "line": node.lineno,
            }
        )
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.functions.append(
            {
                "name": node.name,
                "line": node.lineno,
                "is_async": False,
                "arguments": [arg.arg for arg in node.args.args],
            }
        )
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.functions.append(
            {
                "name": node.name,
                "line": node.lineno,
                "is_async": True,
                "arguments": [arg.arg for arg in node.args.args],
            }
        )
        self.generic_visit(node)