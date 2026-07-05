import ast


class CallGraphVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls = []