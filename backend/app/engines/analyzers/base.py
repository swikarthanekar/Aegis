from abc import ABC, abstractmethod
from pathlib import Path


class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, file_path: Path) -> dict:
        pass