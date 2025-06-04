# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a JSON library testing and reference project that compares different Python JSON packages (json, ujson, orjson, simplejson, msgspec) across various data types. The project specifically tests edge cases like NaN, infinity, and complex Python objects that standard JSON doesn't handle well.

## Commands

### Testing
- `poe test` - Run all tests with benchmark columns for stddev and iqr
- `pytest` - Run tests without benchmark output
- `pytest tests/test_jsons.py::test_encode` - Run only encoding tests
- `pytest tests/test_jsons.py::test_decode` - Run only decoding tests

### Linting
- `ruff check` - Run linter (configured to select ALL rules with specific ignores)
- `ruff format` - Format code

## Architecture

### Test Structure
The core testing framework uses pytest with parametrized tests to create a matrix of:
- **Data types**: Various Python objects including pandas/numpy types, datetime objects, special floats (NaN, inf), etc.
- **JSON libraries**: json, ujson, orjson, simplejson, msgspec

### Key Components
- `tests/test_jsons.py`: Main test file with `test_encode` and `test_decode` parametrized tests
- `tests/conftest.py`: Custom pytest hook that generates a colored matrix showing which library/datatype combinations pass/fail
- `data` dict in test_jsons.py: Comprehensive collection of edge-case Python objects for testing

### Custom Assertion
`assert_almost_equal_with_nan()` handles NaN equality and floating-point comparisons that standard assertions can't handle.

### Test Output
The custom pytest terminal reporter creates a GitHub-flavored table showing test results in a matrix format with colored PASS/FAIL/SKIP indicators for each library-datatype combination.