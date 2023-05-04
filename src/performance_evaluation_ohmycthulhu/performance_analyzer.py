import time
from typing import Union
from .output_analyzer import OutputAnalyzer, OutputAnalyzerResult
from .program_result import ProgramResult
from .examples import AlgorithmTestCase


class PerformanceAnalyzerResultItem:
    def __init__(self, test_case: AlgorithmTestCase, elapsed_time: float, checkpoints: Union[list[hash], None]):
        self._test_case = test_case
        self._elapsed_time = elapsed_time
        self._checkpoints = checkpoints

    def __str__(self):
        return f"Example ({self._test_case.key}): {self._test_case}\nTime (in s): {self._elapsed_time}\n{self.__str_checkpoints__()}"

    def __str_checkpoints__(self):
        if self._checkpoints is None:
            return ''
        header = 'Checkpoints:'
        body = "\n".join([f"{checkpoint['from']} => {checkpoint['to']}: {checkpoint['duration']}" for checkpoint in self._checkpoints])
        return f"{header}\n{body}"


class PerformanceAnalyzerResult(OutputAnalyzerResult):
    def __init__(self, items: list[PerformanceAnalyzerResultItem]):
        self._items = items

    def __str__(self):
        return "Performance analysis:\n" + ('\n' + '*' * 10 + '\n').join([str(x) for x in self._items])


class PerformanceAnalyzer(OutputAnalyzer):
    def __init__(self):
        self._timers = {}

    def name(self):
        return 'Performance Analyzer'

    def before_test_case(self, test_case: AlgorithmTestCase):
        self._timers[test_case.key] = {
            'begin': time.time(),
            'end': None,
        }

    def after_test_case(self, test_case: AlgorithmTestCase, algorithm_result):
        self._timers[test_case.key]['end'] = time.time()

    def analyze(self, examples: list[ProgramResult]) -> OutputAnalyzerResult:
        return PerformanceAnalyzerResult(
            [self._analyze_item(example) for example in examples]
        )

    def analyze_example(self, example: ProgramResult) -> OutputAnalyzerResult:
        return PerformanceAnalyzerResult([self._analyze_item(example)])

    def _analyze_item(self, example: ProgramResult) -> PerformanceAnalyzerResultItem:
        timer = self._timers[example.test_case.key]

        return PerformanceAnalyzerResultItem(
            test_case=example.test_case,
            elapsed_time=timer['end'] - timer['begin'],
            checkpoints=self._measure_checkpoints(example.meta['checkpoints']) if 'checkpoints' in example.meta else None
        )

    @staticmethod
    def _measure_checkpoints(checkpoints):
        points = list(checkpoints.items())
        return [
            {
                'from': start_pos[0],
                'to': end_pos[0],
                'duration': end_pos[1] - start_pos[1]
            } for start_pos, end_pos in zip(points[:-1], points[1:])
        ]