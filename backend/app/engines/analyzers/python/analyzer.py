from pathlib import Path

from app.engines.analyzers.base import BaseAnalyzer
from app.engines.analyzers.python.models import PythonAnalysis
from app.engines.analyzers.python.parser import parse_python_file
from app.engines.analyzers.python.visitors.import_visitor import ImportVisitor
from app.engines.analyzers.python.visitors.symbol_visitor import SymbolVisitor
from app.engines.analyzers.python.models import (
    ClassInfo,
    FunctionInfo,
    PythonAnalysis,
)

class PythonAnalyzer(BaseAnalyzer):
    def analyze(self, file_path: Path) -> PythonAnalysis:
        tree = parse_python_file(file_path)

        import_visitor = ImportVisitor()
        symbol_visitor = SymbolVisitor()

        import_visitor.visit(tree)
        symbol_visitor.visit(tree)

        return PythonAnalysis(
            imports=import_visitor.imports,
            classes=[
                ClassInfo(**cls)
                for cls in symbol_visitor.classes
            ],
            functions=[
                FunctionInfo(**func)
                for func in symbol_visitor.functions
            ]
        )