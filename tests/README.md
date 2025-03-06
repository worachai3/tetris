# Tetris Game Tests

This directory contains test suites for the Tetris game components.

## Running Tests

To run all tests:
```bash
python -m pytest
```

To run specific test file:
```bash
python -m pytest tests/test_tetromino.py
```

To run with coverage report:
```bash
python -m pytest --cov=src tests/
```

## Test Structure

- `test_tetromino.py`: Tests for Tetromino piece behavior
- More test files will be added for:
  - Board mechanics
  - Game state management
  - Score calculations
  - Input handling

## Writing Tests

When adding new tests:
1. Create a new file named `test_*.py`
2. Use unittest.TestCase or pytest style
3. Include docstrings explaining test purposes
4. Follow existing test patterns