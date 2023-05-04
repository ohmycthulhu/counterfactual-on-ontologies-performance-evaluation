from typing import Callable
import owlready2 as owl
from .examples import ExamplesManager, AlgorithmTestCase
from .adapter import AlgorithmAdapter
from .program_result import ProgramResult
from .output_analyzer import OutputAnalyzer, OutputAnalyzerResult


class Program:
    def __init__(self, algorithm: AlgorithmAdapter, analyzers: list[OutputAnalyzer], example_manager: ExamplesManager=None, callbacks: Callable[[list[OutputAnalyzerResult]], None] = None):
        self._examples_manager = example_manager if example_manager is not None else ExamplesManager()
        self._algorithm = algorithm
        self._analyzers = analyzers
        self._callbacks = callbacks if callbacks is not None else []

    def run(self, examples: list[hash], ontology: owl.Ontology):
        self._load_examples(examples, ontology)

        results = self._run_examples()

        analyzes_result = self._analyze_results(results)

        return results, analyzes_result

    def _load_examples(self, examples: list[hash], ontology: owl.Ontology):
        return self._examples_manager.load(examples, ontology)

    def _run_examples(self):
        return [
            self._run_example(example)
            for example in self._examples_manager.examples
        ]

    def _run_example(self, example: AlgorithmTestCase):
        print(f"Running {example}")
        self._run_before_callback(example)
        algorithm_result, meta = self._algorithm.run(example)
        self._run_after_callback(example, algorithm_result)
        example.destroy()
        result = ProgramResult(example, algorithm_result, meta)
        self._invoke_callbacks(result)

        return result

    def _invoke_callbacks(self, result: ProgramResult):
        analysis = [analyzer.analyze_example(result) for analyzer in self._analyzers]
        for callback in self._callbacks:
            callback(analysis)

    def _analyze_results(self, results):
        return [analyzer.analyze(results) for analyzer in self._analyzers]

    def _run_before_callback(self, example: AlgorithmTestCase):
        for analyzer in self._analyzers:
            analyzer.before_test_case(example)

    def _run_after_callback(self, example: AlgorithmTestCase, run_result):
        for analyzer in self._analyzers:
            analyzer.after_test_case(example, run_result)


