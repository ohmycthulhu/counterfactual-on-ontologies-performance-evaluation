import json
import owlready2 as owl
import os.path


class AlgorithmTestCase:
    def __init__(self, example: hash, ontology):
        self._example = example
        self._ontology = ontology
        self._individual = None

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

    def destroy(self):
        if self._individual is not None:
            owl.destroy_entity(self._individual)
            self._individual = None

    @property
    def expected_changes(self) -> list[hash]:
        return self._example['expectedOutcomes'] if 'expectedOutcomes' in self._example else []

    def _initialize_individual(self) -> owl.NamedIndividual:
        cls = self._get_class(self._ontology, self._example['desiredClass'])
        individual = cls(self._name)

        for assertion_info in self._example['assertions']:
            ind_property = self._get_property(self._ontology, assertion_info['property'])
            target = self._get_or_create_individual(self._ontology, assertion_info['value'])

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
                return instance

        new_individual = base_cls('_'.join([c.name for c in cls]).lower)
        new_individual.is_a = cls
        return new_individual

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
