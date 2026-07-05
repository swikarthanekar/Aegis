import ast
from pathlib import Path


def parse_python_file(file_path: Path) -> ast.Module:
    source = file_path.read_text(encoding="utf-8")
    return ast.parse(source)