from src.adapter import AlgorithmAdapter, CounterfactualExplanation, AssertionChange
from src.examples import AlgorithmTestCase
from .graph_generator import generate_counterfactuals


class CEOAdapter(AlgorithmAdapter):
    _TYPE_MAPPING = {
        'modified': 'modify',
        'added': 'insert',
        'removed': 'remove',
    }

    def run(self, example: AlgorithmTestCase):
        result = generate_counterfactuals(example.ontology, example.individual, example.individual.is_a)

        return [
            self._map_item(individual, info)
            for individual, info in result.items()
        ]

    def _map_item(self, individual, info):
        modifications = self._calculate_modifications(info)

        return CounterfactualExplanation(
            individual=individual,
            sparcity=len(modifications),
            proximity=info['distance'],
            changed_assertions=modifications
        )

    def _calculate_modifications(self, info):
        raw_modifications = info['modifications']

        return [
            self._map_modifications(key, raw_modifications[key]) for key in raw_modifications.keys() if key != 'unmodified'
        ]

    def _map_modifications(self, type, changes):
        return [
            self._map_modification(type, change) for change in changes
        ]

    def _map_modification(self, type, change):
        target = change[-1] if (change is list or change is tuple) else change
        return AssertionChange(
            type=self._TYPE_MAPPING.get(type, f'unknown ({type})'),
            changed_property=target.property,
            value=target.instance.is_a
        )


