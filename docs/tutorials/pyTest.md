## Basic Helpers for PyTest

### 1. Using `@pytest.mark.parametrize`
This decorator allows you to run a test function multiple times with different arguments. 

Syntax:
```python
@pytest.mark.parametrize("arg1, arg2, ...", [
    (value1_1, value1_2, ...),
    (value2_1, value2_2, ...),
    ...
])
def test_function(arg1, arg2, ...):
    # Your test code here
```
- **arg1, arg2, ...**: These are the parameter names that your test fuction will accept
- **value1_1, value1_2, ...**: These are the actual sets of data you wish to pass argumengts to your test function.

### 3. Example

```python
def add(a, b):
    return a + b
```
with test:
```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (4, 5, 9),
    (10, 20, 30),
    (0, 0, 0)
])
def test_add(a, b, expected):
    result = add(a, b)
    assert result == expecte
```