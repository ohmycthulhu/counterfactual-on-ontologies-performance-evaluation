## Identifying changes

Each change is mapped into a structure that contains the following fields:
- `type` - can be on of values `modify`, `remove`, `insert`
- `value` - the current value of the property. May be `None` if the type is `remove`
- `old_value` - the previous value of the property. Exists only for `modify` type

## Interface of output

- Transform changed assertions into string in order to compare:
  - `+- {propertyName}: {old_values} => {new_values}` - for object modification
  - `-  {propertyName}` - for removal
  - `+  {propertyName}  {new_values}` - for insertion
- We need an adapter class that will transform from algorithm-specific output to more precise way

## Interface for example

Examples are list of hashes where each item contain the following fields: 
- `key` - ID of the example
- `desiredClass` - the final class. It may be either `string` or an object with `{name, namespace}`
- `assertions` - the existing assertions in the individual
- `expectedOutcomes` - an optional array of expected counterfactuals. If it's empty or not present, the example is unsuitable for quality assurance (testing ranking):
  - each item contains the following:
    - `modifications` - array of modifications:
      - `type` - `insert`, `remove`, `modify`
      - `property` - iri of the instance's property that has been modified
      - `value` - new instance's classes' iris, used in `insert` and `modify` types. May be either array or a single value, depending on the property.


## Interfaces for classes

### `Program`
Runs the performance evaluation and calculates the results.
Uses adapter to run the algorithm, examples manager to load and validate examples, analyzers for analyzing the results of test examples.
Public interface:
- `run(examples, ontology)` - runs the whole program and returns the results in form of array of `ProgramResult` class objects

### `ProgramResult`
Attribute class that contains following fields:
- `test_case` - test case that has been run
- `result` - list of counterfactual explanations that has been generated

****

### `AlgorithmTestCase`
A class that contains attributes required for running the algorithm. It's loaded and validated by `ExamplesManager`.
Includes lazy loading creating of individuals and means for removing corresponding individuals in ontologies.
- `key` - an ID of the test case
- `ontology` - a reference to the relevant ontology
- `individual` - a lazy loaded property. On the first call or after individual has been deleted, new individual will be created and inserted into the ontology.
- `destroy()` - removes the corresponding individual
- `expected_changes` - list of expected changes for the test case


### `ExamplesManager`
Loads and verifies the examples from the file. It also should be able to utilize ontology in order to get necessary types.
- `load(examples, ontology)` - loads a file with examples, maps them to `AlgorithmTestCase`, and verifies their consistency.
- `examples` - returns list of test cases or raises error if they weren't loaded yet.

****

### `AlgorithmAdapter`
An abstract class that defines methods for executing an algorithm. It provides 
- `run(example)` - where `example` is `AlgorithmTestCase`. Executes the example and returns list of `CounterfactualExplanation`.

### `CEOAdapter`
Implements `AlgorithmAdapter` and serves as a bridge for using CEO (Counterfactual Explanations for Ontologies) algorithm.


### `AssertionChange`
Represents a single change of the assertion. May be of three types: `insert`, `remove`, or `modify`.
Contains the following fields:
- `type` - contains the type of change
- `changed_property` - contains a link to the object property that has been changed
- `old_value` - old value of the property, may be `None` if the change type is not `modify`.
- `value` - the current value of the property, may be `None` if the assertion is not present anymore.

### `CounterfactualExplanation`
Attribute class that contains following fields:
- `individual` - individual in OWL terms
- `changed_assertions` - list of changed assertions (`AssertionChange`) (see "Interface of output")
- `proximity` - value of proximity for the given counterfactual
- `sparcity` - value of proximity for the given counterfactual


****


### OutputAnalyzerResult

An attribute class representing the result of `OutputAnalyzer`. The main feature is that defines string interface that is used to display and save the results.

### OutputAnalyzer

A class that encapsulates logic for of analyzing the results of the work. It also provides functionality for callbacks before and after the execution of each test case.
The result of the output analyzer is `OutputAnalyzerResult`. Both of the classes are implemented together to provide full information. 
Available methods for implementing:
- `analyze`\* - processes the results of all example tests and outputs `OutputAnalyzerResult`'s descendant as result.
- `before_test_case` - callback that is called on test case right before it's executed
- `after_test_case` - callback that is called on test case right after it's executed
