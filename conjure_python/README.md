# Conjure Python Interface

This directory contains the Python interface for the Conjure constraint solver.

## Directory Structure

```
conjure_python/
├── __init__.py
├── conjure.py           # Main interface to Conjure solver
├── conjure_cache.py     # Caching mechanism for Conjure operations
├── essence_types/       # Essence type implementations
│   ├── __init__.py
│   ├── base.py         # Base class for all Essence types
│   ├── function.py     # Function type implementation
│   ├── helpers.py      # Type checking and conversion utilities
│   ├── matrix.py       # Matrix type implementation
│   ├── record.py       # Record type implementation
│   ├── relation.py     # Relation type implementation
│   ├── sequence.py     # Sequence type implementation
│   ├── set.py         # Set type implementation
│   └── tuple.py       # Tuple type implementation
├── model.py           # Essence model representation and solver configuration
└── solution.py        # Solution representation and processing
```

## Core Components

### 1. `conjure.py`
Main interface class that provides:
- Solver interaction
- Model parameter handling
- Solution retrieval
- Solver configuration

### 2. `model.py`
Handles Essence model representation:
- Constraint management
- Parameter handling
- Solver configuration
- Model solving

### 3. `solution.py`
Manages solution representation:
- Raw solution access
- Python-native solution conversion
- Solution iteration
- Solution state management

### 4. `conjure_cache.py`
Provides caching functionality:
- Cache management
- Cache persistence
- Cache invalidation
- Performance optimization

## Implementation Guidelines

### Code Style
- Use type hints for all parameters and return values
- Follow Python's standard docstring format
- Use consistent spacing (4 spaces for indentation)
- Use snake_case for function and variable names
- Use PascalCase for class names