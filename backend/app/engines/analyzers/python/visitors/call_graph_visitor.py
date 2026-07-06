import ast
from app.utils.ast_utils import resolve_expression


class CallGraphVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls = []
        self.assignments = {}

        self.current_function = None
        self.current_class = None

    # ----------------------------
    # Class tracking
    # ----------------------------
    def visit_ClassDef(self, node: ast.ClassDef):
        prev_class = self.current_class
        self.current_class = node.name

        self.generic_visit(node)

        self.current_class = prev_class

    # ----------------------------
    # Function tracking
    # ----------------------------
    def visit_FunctionDef(self, node: ast.FunctionDef):
        prev_func = self.current_function

        if self.current_class:
            self.current_function = f"{self.current_class}.{node.name}"
        else:
            self.current_function = node.name

        self.generic_visit(node)

        self.current_function = prev_func

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef(node)

    # ----------------------------
    # Assignment tracking
    # ----------------------------
    def visit_Assign(self, node: ast.Assign):
        if not node.targets:
            return

        target = node.targets[0]

        # handle: self.memory = Memory()
        if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
            obj = target.value.id   # self
            attr = target.attr      # memory

            key = f"{obj}.{attr}"

            if (
                isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
            ):
                self.assignments[key] = node.value.func.id

        self.generic_visit(node)

    # ----------------------------
    # Call resolution (FIXED)
    # ----------------------------
    def visit_Call(self, node: ast.Call):
        if not self.current_function:
            self.generic_visit(node)
            return

        raw = resolve_expression(node.func)

        callee = raw

        parts = raw.split(".")

        # CASE 1: self.memory.save()
        if len(parts) >= 3:
            obj_key = f"{parts[0]}.{parts[1]}"  # self.memory

            if obj_key in self.assignments:
                class_name = self.assignments[obj_key]
                parts[1] = class_name
                callee = ".".join(parts)

        # CASE 2: direct calls (helper(), print())
        elif len(parts) == 1:
            callee = parts[0]

        if callee != "<unknown>":
            self.calls.append({
                "caller": self.current_function,
                "callee": callee,
                "line": node.lineno,
            })

        self.generic_visit(node)