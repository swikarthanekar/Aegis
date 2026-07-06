import ast


class AssignmentVisitor(ast.NodeVisitor):
    def __init__(self):
        self.assignments = {}

    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Attribute):
            target = node.targets[0]

            if isinstance(target.value, ast.Name):
                var = f"{target.value.id}.{target.attr}"
            else:
                var = target.attr

            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                self.assignments[var] = node.value.func.id

        self.generic_visit(node)