from abc import ABC, abstractmethod

class AlgorithmAdapter(ABC):
    # TODO: Add type hint
    @abstractmethod
    def run(self, example):
        pass


class CounterfactualExplanation:
    # TODO: Add type hint
    def __init__(self, individual, changed_assertions, proximity, sparcity):
        self._individual = individual
        self._changed_assertions = changed_assertions
        self._proximity = proximity
        self._sparcity = sparcity

    # TODO: Add getters for individual, changed assertions, proximity, and sparcity
