# XLBricks unit tests

## Running tests

From the project root (parent of `xlbricks` and `tests`):

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Or with pytest:

```bash
python -m pytest tests/ -v
```

## Test modules

- **test_validation.py** – Tests for `xlbricks.libs.validation` (`_is_missing`, `_check_required`, `_check_array_2d`).  
  **Requires:** `numpy` only. No PyQt5 or QuantLib. Always runnable.

- **test_xlbfunctions.py** – Tests for all `xlb_*` UDF entry points (validation + success paths with `persist=False`).  
  **Requires:** `numpy`, `pandas`, `xlwings`, `PyQt5`, `QuantLib`.  
  If any dependency is missing, these tests are **skipped** with a clear reason; the rest of the suite still runs.

## Coverage

- **Validation:** Missing/empty/NaN inputs, wrong types, empty arrays, `allow_none`.
- **xlbfunctions:** Each `xlb_*` has tests for missing required args and invalid inputs (returns `#XLB ERROR: ...`), and success-path tests where applicable (brick/array/list/table/grid/create_function/merge/today/clear_bricks_front, etc.).
- **Edge cases:** Empty key/alias, NaN function_name, empty 2D data, decorator exception handling.
