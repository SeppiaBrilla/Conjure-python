# Essence Types Implementation

This directory contains the implementation of all Essence language types in Python.

## Directory Structure

```
essence_types/
├── __init__.py
├── base.py         # Base class for all Essence types
├── function.py     # Function type implementation
├── helpers.py      # Type checking and conversion utilities
├── matrix.py       # Matrix type implementation
├── record.py       # Record type implementation
├── relation.py     # Relation type implementation
├── sequence.py     # Sequence type implementation
├── set.py         # Set type implementation
└── tuple.py       # Tuple type implementation
```

## Type Implementation Guidelines

### Base Class
All types inherit from `EssenceType` in `base.py` which provides:
- Common type conversion methods
- Base type checking functionality
- Standard iteration and indexing support

### Type-Specific Implementations
Each type file implements:
1. Type-specific conversion from Essence to Python
2. Appropriate type checking
3. Support for iteration and indexing where applicable
4. Proper string representation
5. Type-specific methods

### Type Parameters
All type classes accept:
- `values`: The actual values of the type
- `essence_types`: String representation of types in the Essence language

## Type System

### Core Types
- `base.py`: Base class for all Essence types
- `function.py`: Function type with domain and codomain
- `matrix.py`: Multi-dimensional matrix type
- `record.py`: Record type with named fields
- `relation.py`: Relation type for representing relationships
- `sequence.py`: Sequence type for ordered collections
- `set.py`: Set type for unordered collections
- `tuple.py`: Tuple type for fixed-size collections

### Helpers
- `helpers.py`: Contains utility functions for:
  - Type checking
  - Type conversion
  - Type validation
  - Type parsing from Essence strings

## Implementation Requirements

1. All methods must have proper type hints
2. All classes must have comprehensive docstrings
3. Type conversion must be bidirectional
4. Error handling must be clear and specific
5. Type checking must be thorough

## Contributing to Types

When adding a new type:
1. Create a new file following the naming convention
2. Inherit from `EssenceType`
3. Implement all required methods
4. Add comprehensive tests
5. Ensure proper type hints and docstrings
