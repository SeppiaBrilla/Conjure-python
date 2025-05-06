# Conjure-python

A Python interface for solving constraint problems using Conjure and the Essence language.

## Overview

Conjure-python provides a Python interface to interact with Conjure, a constraint solver that uses the Essence language for problem specification. The library allows you to:

1. Define constraint problems using Essence syntax
2. Solve problems using different solvers
3. Access solutions in both raw and Python-native formats
4. Work with various Essence data types as native Python objects

## Core Components

### EssenceModel
The main class for defining and solving constraint problems:
- Add constraints using Essence syntax
- Set solver configurations
- Add parameters
- Solve the model
- Access solutions

### EssenceSolution
Represents solutions to constraint problems:
- Access solutions in raw or Python-native format
- Iterate over multiple solutions
- Get solution state (SAT/UNSAT)
- Convert solutions to string format

## Implemented Types

All types inherit from `EssenceType` and share common characteristics:

### Common Type Characteristics
- Type conversion from Essence to Python
- Type checking and validation
- String representation
- Iteration support (where applicable)
- Type-specific methods

### Collection Types
- **Matrix**: Multi-dimensional array with shape information
  - Methods: `shape()`, `__getitem__()` with nested indices
  - Supports: Indexing by multiple indices

- **Sequence**: Ordered collection of elements
  - Methods: `__getitem__()` with integer indices
  - Supports: Length, iteration

- **Set**: Unordered collection of unique elements
  - Methods: `__getitem__()` with integer indices
  - Supports: Length, iteration

- **Tuple**: Fixed-size ordered collection
  - Methods: `__getitem__()` with integer indices
  - Supports: Length, iteration

### Structured Types
- **Record**: Named fields with specific types
  - Methods: `keys()`, `values()`, `items()`
  - Supports: Field access by name

- **Relation**: Collection of tuples representing relationships
  - Methods: `__getitem__()` with nested indices
  - Supports: Length, iteration

### Mapping Types
- **Function**: Maps domain to codomain
  - Methods: `__getitem__()` with domain values
  - Supports: Domain and codomain type checking

### Basic Types
- **Integer**: Numeric values
- **Boolean**: True/False values

## Usage Example

```python
from conjure_python import EssenceModel

# Create model
model = EssenceModel()

# Add constraints
model.append("find x: int(0..10)")
model.append("find y: int(0..10)")
model.append("given z: int(0..10)")
model.append("x + y = z")

# Set solver
model.set_solver("chuffed")

# Add parameters
model.add_parameters("z", 5)

# Solve
solutions = model.solve()

# Access solutions
if solutions.state == "SAT":
    for sol in solutions:
        print(sol)  # Prints solutions in Python-native format
else:
    print("No solution found")
```
## check for conjure 
if you want to check if conjure is available on your system by using the ```is_conjure_available()``` function which returns a boolean value.
```py
from conjure_python import is_conjure_available
print("Is conjure available?", is_conjure_available())
```
