from abc import ABC, abstractmethod
from examples import AlgorithmTestCase
import owlready2 as owl


class AlgorithmAdapter(ABC):
    @abstractmethod
    def run(self, example: AlgorithmTestCase):
        pass


class AssertionChange:
    _INDICATORS = {
        'insert': '+ ',
        'remove': '- ',
        'modify': '+-',
    }

    def __init__(self, type, changed_property, value=None):
        self._type = type
        self._changed_property = changed_property
        self._value = value

    @property
    def type(self):
        return self._type

    @property
    def changed_property(self):
        return self._changed_property

    @property
    def value(self):
        return self._value

    def __str__(self):
        return f"{self._indicator()} {self._changed_property}{f' {self._value}' if self._value else ''}"

    def _indicator(self):
        return self._INDICATORS.get(self._type, '? ')


class CounterfactualExplanation:
    def __init__(self, individual: owl.NamedIndividual, changed_assertions: list[AssertionChange], proximity: float, sparcity: int):
        self._individual = individual
        self._changed_assertions = changed_assertions
        self._proximity = proximity
        self._sparcity = sparcity

    @property
    def individual(self):
        return self._individual

    @property
    def changed_assertions(self):
        return self._changed_assertions

    @property
    def sparcity(self):
        return self._sparcity

    @property
    def proximity(self):
        return self._proximity

    def __str__(self):
        return "\n".join([str(change) for change in self._changed_assertions])



