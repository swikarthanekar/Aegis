import ast


class CallGraphVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls = []
        self.current_function = None

    def visit_FunctionDef(self, node):
        previous = self.current_function
        self.current_function = node.name

        self.generic_visit(node)

        self.current_function = previous

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_Call(self, node):
        if self.current_function:
            if isinstance(node.func, ast.Name):
                self.calls.append({
                    "caller": self.current_function,
                    "callee": node.func.id,
                    "line": node.lineno,
                })

        self.generic_visit(node)