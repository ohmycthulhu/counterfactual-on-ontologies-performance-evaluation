from abc import ABC, abstractmethod
from program_result import ProgramResult


class OutputAnalyzerResult(ABC):
    @abstractmethod
    def __str__(self):
        pass


class OutputAnalyzer(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def analyze(self, examples: list[ProgramResult]) -> OutputAnalyzerResult:
        pass
