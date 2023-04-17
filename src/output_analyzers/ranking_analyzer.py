from src.output_analyzer import OutputAnalyzer, OutputAnalyzerResult
from src.program_result import ProgramResult
from src.adapter import CounterfactualExplanation, AssertionChange
from typing import Union


class RankingAnalyzerResultItem:
    def __init__(self, ranks: list[int], explanations: list[CounterfactualExplanation], test_case):
        self._ranks = ranks
        self._explanations = explanations
        self._test_case = test_case

    def __str__(self):
        return f"Example: {self._test_case}\nRanking:\n{self.__str_explanations__()}"

    def __str_explanations__(self):
        return "\n\n".join([
            self._str_explanation(explanation, index) for index, explanation in enumerate(self._explanations)
        ])

    def _str_explanation(self, explanation, index):
        is_expected = self._ranks.count(index) > 0
        return f"Explanation #{index + 1} {'(expected)' if is_expected else ''}\n{explanation}"


class RankingAnalyzerResult(OutputAnalyzerResult):
    def __init__(self, items: list[RankingAnalyzerResultItem]):
        self._items = items

    def __str__(self):
        return "Ranking analysis:\n" + ('\n' + '*' * 10 + '\n').join([str(x) for x in self._items])


class RankingAnalyzer(OutputAnalyzer):
    def name(self):
        return 'Ranking Analyzer'

    def analyze(self, examples: list[ProgramResult]) -> OutputAnalyzerResult:
        return RankingAnalyzerResult(
            [self._analyze_item(example) for example in examples]
        )

    def _analyze_item(self, example: ProgramResult) -> RankingAnalyzerResultItem:
        return RankingAnalyzerResultItem(
            ranks=self._get_ranks(example.result, example.test_case.expected_changes),
            explanations=example.result,
            test_case=example.test_case
        )

    def _get_ranks(self, explanations: list[CounterfactualExplanation], expectations: hash) -> list[int]:
        return [
            index
            for index, explanation in enumerate(explanations)
            if self._is_explanation_expected(explanation, expectations)
        ]

    def _is_explanation_expected(self, explanation: CounterfactualExplanation, expected_explanations: list[hash]) -> bool:
        for expected_explanation in expected_explanations:
            if self._are_assertions_expected(explanation.changed_assertions, expected_explanation['modifications']):
                return True

        return False

    def _are_assertions_expected(self, changed: list[AssertionChange], expected: list[hash]):
        assertions_left = list(expected)

        for changed_assertion in changed:
            if len(assertions_left) == 0:
                return False

            expected_assertion = self._find_expected_assertion(changed_assertion, assertions_left)

            if expected_assertion is None:
                return False

            assertions_left.remove(expected_assertion)

        return len(assertions_left) == 0

    @staticmethod
    def _find_expected_assertion(changed_assertion: AssertionChange, expected_pool: list[hash]):
        # The change is performed in three stages:
        # - type of change
        # - property that has been changed
        # - what is the final value
        # depending on the type of the change, value may not be present
        # depending on the type of property, value may be either list or single value
        for expected_change in expected_pool:
            if expected_change['type'] != changed_assertion.type:
                continue
            if expected_change['property'] != changed_assertion.changed_property.iri:
                continue
            if not ('new_value' in expected_change or changed_assertion.value):
                return expected_change

            # Check whether value is iterable
            if isinstance(changed_assertion.value, Union[list, tuple]):
                # If they are, check them as sets
                if set(expected_change['new_value']) == set(value.iri for value in changed_assertion.value):
                    return expected_change
            else:
                # Otherwise, check directly
                if expected_change['new_value'] == changed_assertion.value.iri:
                    return expected_change

        return None
