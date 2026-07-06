import ast


def resolve_expression(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        parent = resolve_expression(node.value)
        return f"{parent}.{node.attr}"

    if isinstance(node, ast.Call):
        return resolve_expression(node.func)

    if isinstance(node, ast.Constant):
        return repr(node.value)

    return "<unknown>"