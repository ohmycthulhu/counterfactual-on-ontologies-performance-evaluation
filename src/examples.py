class ExamplesManager:
    def __init__(self):
        self._ontologies = {}

    # TODO: Add type hint
    def load(self, path):
        # TODO: Plan
        # TODO: Implement
        pass

    # TODO: Add type hint
    def _get_ontology(self, path):
        # TODO: Implement loading or returning from cache
        pass

    # TODO: Add type hint
    def _verify_examples(self, examples):
        # TODO: Plan
        # TODO: Implement
        # TODO: Raise exception if any of test cases are invalid or there are collisions in test case keys
        pass


class AlgorithmTestCase:
    # TODO: Add type hint
    def __init__(self, example):
        self._example = example
        self._individual = self._initialize_individual(example)

    # TODO: Add getters for individual

    def _initialize_individual(self):
        # TODO: Implement
        return None

    def is_valid(self):
        # TODO: Implement
        return False
