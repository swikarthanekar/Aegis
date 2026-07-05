from pathlib import Path

from app.engines.analyzers.base import BaseAnalyzer
from app.engines.analyzers.python_analyzer import PythonAnalyzer


ANALYZERS: dict[str, type[BaseAnalyzer]] = {
    ".py": PythonAnalyzer,
}


def get_analyzer(file_path: Path) -> BaseAnalyzer | None:
    analyzer = ANALYZERS.get(file_path.suffix.lower())

    if analyzer is None:
        return None

    return analyzer()