from src.adapter import AlgorithmAdapter, CounterfactualExplanation, AssertionChange
from src.examples import AlgorithmTestCase
from .graph_generator import generate_counterfactuals
from typing import Union
from functools import reduce


class CEOAdapter(AlgorithmAdapter):
    _TYPE_MAPPING = {
        'modified': 'modify',
        'added': 'insert',
        'removed': 'remove',
    }

    def run(self, example: AlgorithmTestCase):
        counterfactuals = generate_counterfactuals(example.ontology, example.individual, example.individual.is_a)

        run_results = [
            self._map_item(individual, info)
            for individual, info in counterfactuals.items()
        ]

        example.destroy()

        return run_results

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

        # Flatten the list into 1D
        return reduce(lambda acc, arr: [*acc, *arr], [
            [self._map_modification(key, change) for change in changes]
            for key, changes in raw_modifications.items() if key != 'unmodified'
        ])

    def _map_modifications(self, type, changes):
        return [
            self._map_modification(type, change) for change in changes
        ]

    def _map_modification(self, type, change):
        target = change
        old_value, new_value = None, None

        if isinstance(target, Union[list, tuple]):
            if len(target) >= 2:
                old_value = target[-2].instance
                new_value = target[-1].instance
                target = target[-1]
            else:
                target = target[0]
                new_value = target.instance
        else:
            new_value = target.instance

        return AssertionChange(
            type=self._TYPE_MAPPING.get(type, f'unknown ({type})'),
            changed_property=target.property,
            old_value=old_value.is_a if old_value is not None else None,
            value=new_value.is_a if new_value is not None else None
        )


