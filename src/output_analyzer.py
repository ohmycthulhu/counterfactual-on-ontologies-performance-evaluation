from abc import ABC, abstractmethod
from examples import AlgorithmTestCase
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

    def before_test_case(self, test_case: AlgorithmTestCase):
        pass

    def after_test_case(self, test_case: AlgorithmTestCase, algorithm_result):
        pass
