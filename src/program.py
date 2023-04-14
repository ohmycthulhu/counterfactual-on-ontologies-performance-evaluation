from examples import ExamplesManager, AlgorithmTestCase
from adapter import AlgorithmAdapter, CounterfactualExplanation


class Program:
    def __init__(self, algorithm: AlgorithmAdapter):
        self._examples_manager = ExamplesManager()
        self._algorithm = algorithm

    def run(self, examples_path: str):
        self._load_examples(examples_path)

        result = self._run_examples()

        return result

    def _load_examples(self, examples_path):
        return self._examples_manager.load(examples_path)

    def _run_examples(self):
        return [
            ProgramResult(example, self._algorithm.run(example))
            for example in self._examples_manager.examples
        ]


class ProgramResult:
    def __init__(self, test_case: AlgorithmTestCase, explanations: list[CounterfactualExplanation]):
        self._test_case = test_case
        self._explanations = explanations

    @property
    def test_case(self):
        return self._test_case

    @property
    def result(self):
        return self._explanations
