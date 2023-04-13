## Interface of output

- Transform changed assertions into string in order to compare:
  - `+- {propertyName}: {old_values} => {new_values}` - for object modification
  - `-  {propertyName}` - for removal
  - `+  {propertyName}  {new_values}` - for insertion
  - P.S. sort the classes in `old_values` and `new_values` to ensure that the comparison is correct
- We need an adapter class that will transform from algorithm-specific output to more precise way

## Interface for example

- `key` - ID of the example
- `ontology` - path to the ontology
- `desiredClass` - the final class. It may be either `string` or an object with `{name, namespace}`
- `assertions` - the existing assertions in the individual
- `expectedOutcomes` - an array of expected counterfactuals. If it's empty or not present, the example is unsuitable for quality assurance (testing ranking):
  - each item contains the following:
    - `modifications` - array of modifications:
      - `type` - `insert`, `delete`, `modify`
      - `property` - instance's property that has been modified
      - `new_value` - new instance's classes, used in `insert` and `modify` types


## Interfaces for classes

### `Program`
Runs the performance evaluation and calculates the results. Uses adapter to run the algorithm, and config manager to load and validate examples.
- `run(examples_path)` - runs the whole program and returns the results in form of array of `ProgramResult` class objects
- `_load_examples()` - uses `ExamplesManager` to load examples. Raises error if there is an error in examples file. Returns list of `AlgorithmTestCases`

### `ProgramResult`
Attribute class that contains following fields:
- `example_id` - ID of the example
- `_example` - an object of the example
- `rank` - number of ranked counterfactual

****

### `AlgorithmTestCase`
A class that contains attributes required for running the algorithm. It's loaded and validated by `ExamplesManager`.
- `_example` - an object of the example
- `individual()` - generates an individual that may be added into ontology
- `is_valid()` - checks the existence of used classes inside the 


### `ExamplesManager`
Loads and verifies the examples from the file. It also should be able to utilize ontology in order to get necessary types.
- `load(path)` - loads a file with examples, maps them to `AlgorithmTestCase`, and verifies their consistency.
- `_get_ontology(path)` - loads or returns already loaded ontology
- `_verify_examples(examples)` - verifies examples in form of `AlgorithmTestCase`

****

### `AlgorithmAdapter`
An abstract class that defines methods for executing an algorithm. It provides 
- `run(example)` - where `example` is `AlgorithmTestCase`. Executes the example and returns list of `CounterfactualExplanation`.

### `CEOAdapter`
Implements `AlgorithmAdapter` and serves as a bridge for using CEO (Counterfactual Explanations for Ontologies) algorithm.


### `CounterfactualExplanation`
Attribute class that contains following fields:
- `individual` - individual in OWL terms
- `changed_assertions` - list of changed assertions in string format (see "Interface of output")
- `proximity` - value of proximity for the given counterfactual
- `sparcity` - value of proximity for the given counterfactual
