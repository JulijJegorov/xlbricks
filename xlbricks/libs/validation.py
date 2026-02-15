"""
    Author: julij.jegorov
    Date: 15/02/2026
    Description: Validation helpers for UDF inputs: _is_missing, _check_required, _check_array_2d.
                 Used by xlbfunctions; no heavy deps (numpy only) so tests can run without PyQt/QuantLib.
"""

import numpy as np

_ERROR_PREFIX = '#XLB ERROR: '


def _is_missing(val):
    """True if value is missing, empty, or not properly defined for use as input."""
    if val is None:
        return True
    if isinstance(val, float) and np.isnan(val):
        return True
    if isinstance(val, str) and (not val.strip() or val.strip().lower() == 'nan'):
        return True
    if hasattr(val, 'shape'):
        if val.size == 0:
            return True
        if getattr(val, 'dtype', None) is not None and np.issubdtype(val.dtype, np.floating):
            try:
                if np.all(np.isnan(val)):
                    return True
            except (TypeError, ValueError):
                pass
    return False


def _check_required(name, val, allow_none=False):
    """Return an error string if required value is missing, else None."""
    if allow_none and val is None:
        return None
    if _is_missing(val):
        return _ERROR_PREFIX + '%s is required and cannot be empty.' % name
    return None


def _check_array_2d(name, val, required=True):
    """Return an error string if value is not a 2D array (when required), else None."""
    if val is None and not required:
        return None
    if val is None:
        return _ERROR_PREFIX + '%s is required.' % name
    if not hasattr(val, 'shape') or len(val.shape) != 2:
        return _ERROR_PREFIX + '%s must be a 2D range (array).' % name
    if val.size == 0:
        return _ERROR_PREFIX + '%s cannot be empty.' % name
    return None
