from examples import ExamplesManager, AlgorithmTestCase
from adapter import AlgorithmAdapter
from program_result import ProgramResult
from output_analyzer import OutputAnalyzer


class Program:
    def __init__(self, algorithm: AlgorithmAdapter, analyzers: list[OutputAnalyzer]):
        self._examples_manager = ExamplesManager()
        self._algorithm = algorithm
        self._analyzers = analyzers

    def run(self, examples_path: str):
        self._load_examples(examples_path)

        results = self._run_examples()

        analyzes_result = self._analyze_results(results)

        return results, analyzes_result

    def _load_examples(self, examples_path):
        return self._examples_manager.load(examples_path)

    def _run_examples(self):
        return [
            ProgramResult(example, self._algorithm.run(example))
            for example in self._examples_manager.examples
        ]

    def _run_example(self, example: AlgorithmTestCase):
        self._run_before_callback(example)
        algorithm_result = self._algorithm.run(example)
        self._run_after_callback(example, algorithm_result)
        example.destroy()
        return ProgramResult(example, algorithm_result)

    def _analyze_results(self, results):
        return [analyzer.analyze(results) for analyzer in self._analyzers]

    def _run_before_callback(self, example: AlgorithmTestCase):
        for analyzer in self._analyzers:
            analyzer.before_test_case(example)

    def _run_after_callback(self, example: AlgorithmTestCase, run_result):
        for analyzer in self._analyzers:
            analyzer.after_test_case(example, run_result)


