from .examples import AlgorithmTestCase
from .adapter import CounterfactualExplanation


class ProgramResult:
    def __init__(self, test_case: AlgorithmTestCase, explanations: list[CounterfactualExplanation], meta: hash):
        self._test_case = test_case
        self._explanations = explanations
        self._meta = meta

    @property
    def test_case(self) -> AlgorithmTestCase:
        return self._test_case

    @property
    def result(self) -> list[CounterfactualExplanation]:
        return self._explanations

    @property
    def meta(self):
        return self._meta
