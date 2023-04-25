import owlready2 as owl
from typing import Union


class AlgorithmTestCase:
    def __init__(self, example: hash, ontology):
        self._example = example
        self._ontology = ontology
        self._individual = None
        self._new_individuals = []

    @property
    def key(self):
        return self._example['key']

    @property
    def ontology(self):
        return self._ontology

    @property
    def _name(self):
        return f"'text-example-{self.key}'"

    @property
    def individual(self) -> owl.NamedIndividual:
        if self._individual is None:
            self._individual = self._initialize_individual()
        return self._individual

    @property
    def desired_class(self):
        desired_cls_iris = self._example['desiredClass']
        if not isinstance(desired_cls_iris, Union[tuple, list]):
            desired_cls_iris = [desired_cls_iris]

        return [self._get_class(self._ontology, iri) for iri in desired_cls_iris]


    @property
    def _primary_class(self):
        primary_cls_iri = self._example['desiredClass']
        if isinstance(primary_cls_iri, Union[tuple, list]):
            primary_cls_iri = primary_cls_iri[0]

        return self._get_class(self._ontology, primary_cls_iri)

    def destroy(self):
        if self._individual is not None:
            owl.destroy_entity(self._individual)
            self._individual = None

        for target in self._new_individuals:
            owl.destroy_entity(target)
            self._individual = None

    @property
    def expected_changes(self) -> list[hash]:
        return self._example['expectedOutcomes'] if 'expectedOutcomes' in self._example else []

    def _initialize_individual(self) -> owl.NamedIndividual:
        individual = owl.Thing(name=self._name, namespace=self._primary_class.namespace)

        for assertion_info in self._example['assertions']:
            ind_property = self._get_property(self._ontology, assertion_info['property'])
            target, is_new = self._get_or_create_individual(self._ontology, assertion_info['value'])

            if is_new:
                self._new_individuals.append(target)

            if owl.FunctionalProperty in ind_property.is_a:
                setattr(individual, ind_property.name, target)
            else:
                individual.__getattr__(ind_property.name).append(target)

        return individual

    @staticmethod
    def _get_class(ontology, iri):
        for cls in ontology.classes():
            if cls.iri == iri:
                return cls

        raise Exception(f"{iri} was not found")

    @staticmethod
    def _get_property(ontology, iri):
        for cls in ontology.properties():
            if cls.iri == iri:
                return cls

        raise Exception(f"{iri} was not found")

    @staticmethod
    def _get_or_create_individual(ontology, is_a):
        cls = [AlgorithmTestCase._get_class(ontology, c) for c in is_a]

        base_cls = cls[0]
        instances = base_cls.instances()

        for instance in instances:
            if set(instance.is_a) == set(cls):
                return instance, False

        new_individual = base_cls('_'.join([c.name for c in cls]).lower())
        new_individual.is_a = cls
        return new_individual, True

    def __str__(self):
        return f"{self.__str_assertions__()} => {self._example['desiredClass']}"

    def __str_assertions__(self):
        return ' and '.join([self.__str_assertion__(assertion) for assertion in self._example['assertions']])

    @staticmethod
    def __str_assertion__(assertion):
        return f"({assertion['property']} {assertion['value']})"


class ExamplesManager:
    def __init__(self):
        self._ontologies = {}
        self._examples = []
        self._loaded = False

    @property
    def examples(self) -> list[AlgorithmTestCase]:
        if not self._loaded:
            raise RuntimeError("Examples has not been loaded yet")

        return self._examples

    def load(self, examples: list[hash], ontology: owl.Ontology):
        self._verify_examples(examples)
        examples = self._load_examples(examples, ontology)
        self._ensure_test_cases_are_consistent(examples)

        self._examples = examples
        self._loaded = True

        return self._examples

    def _load_examples(self, examples: list[hash], ontology):
        return [AlgorithmTestCase(example, ontology) for example in examples]

    def _verify_examples(self, examples: list[hash]):
        keys = [example['key'] for example in examples]
        unique_keys = set(keys)
        duplicate_keys = [key for key in unique_keys if keys.count(key) > 1]

        if duplicate_keys:
            raise Exception(f"Duplicate keys found: {', '.join(duplicate_keys)}")

    def _ensure_test_cases_are_consistent(self, test_cases: list[AlgorithmTestCase]):
        inconsistent_cases = []
        for test_case in test_cases:
            print(f"Checking consistency of {test_case.key}'s {test_case.individual}")
            is_consistent, error = self._ensure_test_case_consistent(test_case)

            if not is_consistent:
                inconsistent_cases.append(test_case)

            test_case.destroy()

        if len(inconsistent_cases):
            raise owl.base.OwlReadyInconsistentOntologyError(
                f"Following test cases are inconsistent: {', '.join([case.key for case in inconsistent_cases])}"
            )

        print("All test cases are consistent", end='\n\n')

    def _ensure_test_case_consistent(self, test_case: AlgorithmTestCase):
        try:
            owl.sync_reasoner(test_case.ontology, debug=0)
        except owl.base.OwlReadyInconsistentOntologyError as error:
            return False, error

        return True, None