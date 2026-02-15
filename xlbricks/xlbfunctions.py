"""
    Author: julij
    Date: 05/10/2022
    Description: 
"""

import sys
import inspect
import os.path as osp
import numpy as np
import xlwings as xw
from datetime import datetime
from functools import wraps
import xlbricks.libs.xlfunctions as xl
from xlbricks.libs.utility_functions import XLUtils

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from xlbricks.ui.explorer import Explorer
from xlbricks.ui.tree_model import DictionaryTreeModel, node_structure_from_dict
from xlbricks.ui.config_editor import show_config_editor
from xlbricks.libs.xlbricks_frontstack import XLBricksFrontStack

# Error prefix so Excel cells show a clear message
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


def _return_errors(f):
    """Decorator: catch exceptions and return a #ERROR: message string for Excel.
    Preserves the wrapped function's signature so xlwings UDF inspection still works."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return _ERROR_PREFIX + '%s: %s' % (type(e).__name__, str(e))
    wrapper.__signature__ = inspect.signature(f)
    return wrapper


@xw.func
@xw.arg('key')
@xw.arg('data', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
@_return_errors
def xlb_brick(key, data, persist=True, xlapp=None):
    err = _check_required('key', key) or _check_array_2d('data', data)
    if err:
        return err
    return xl.xlbrick_create(key, data, persist, xlapp)


@xw.func
@xw.arg('key_1')
@xw.arg('brick_1', np.array, ndim=2)
@xw.arg('key_2')
@xw.arg('brick_2', np.array, ndim=2)
@xw.arg('key_3')
@xw.arg('brick_3', np.array, ndim=2)
@xw.arg('key_4')
@xw.arg('brick_4', np.array, ndim=2)
@xw.arg('key_5')
@xw.arg('brick_5', np.array, ndim=2)
@xw.arg('key_6')
@xw.arg('brick_6', np.array, ndim=2)
@xw.arg('key_7')
@xw.arg('brick_7', np.array, ndim=2)
@xw.arg('key_8')
@xw.arg('brick_8', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
@_return_errors
def xlb_bricks(key_1, brick_1, key_2=None, brick_2=None, key_3=None, brick_3=None,
               key_4=None, brick_4=None, key_5=None, brick_5=None, key_6=None, brick_6=None,
               key_7=None, brick_7=None, key_8=None, brick_8=None, persist=True, xlapp=None):
    err = _check_required('key_1', key_1) or _check_array_2d('brick_1', brick_1)
    if err:
        return err
    return xl.xlbricks_create(key_1, brick_1, key_2, brick_2, key_3, brick_3, key_4, brick_4,
                              key_5, brick_5, key_6, brick_6, key_7, brick_7, key_8, brick_8, persist, xlapp)


@xw.func
@xw.arg('data', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
@_return_errors
def xlb_array(data, persist=True, xlapp=None):
    err = _check_array_2d('data', data)
    if err:
        return err
    return xl.array_create(data, persist, xlapp)


@xw.func
@xw.arg('data', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
@_return_errors
def xlb_list(data, persist=True, xlapp=None):
    err = _check_array_2d('data', data)
    if err:
        return err
    return xl.list_create(data, persist, xlapp)


@xw.func
@xw.arg('data', np.array, ndim=2)
@xw.arg('index', np.array, ndim=2)
@xw.arg('columns', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
@_return_errors
def xlb_table(data, columns=None, index=None, persist=True, xlapp=None):
    err = _check_array_2d('data', data)
    if err:
        return err
    return xl.table_create(data, columns, index, persist, xlapp)


@xw.func
@xw.arg('data', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
@_return_errors
def xlb_grid(data, persist=True, xlapp=None):
    err = _check_array_2d('data', data)
    if err:
        return err
    return xl.grid_create(data, persist, xlapp)


@xw.func
@xw.arg('bricks', np.array, ndim=2)
@xw.arg('keys')
@xw.arg('xlapp', vba='Application')
@_return_errors
def xlb_lookup(bricks, keys=None, persist=True, xlapp=None):
    err = _check_array_2d('bricks', bricks) or _check_required('keys', keys)
    if err:
        return err
    return xl.lookup_element(bricks, keys, persist, xlapp)


@xw.func
@xw.arg('brick', np.array, ndim=2)
@_return_errors
def xlb_flatten(brick):
    err = _check_array_2d('brick', brick)
    if err:
        return err
    return xl.flatten_element(brick)


@xw.func
@xw.arg('brick', np.array, ndim=2)
@_return_errors
def xlb_alias(brick, alias):
    err = _check_array_2d('brick', brick) or _check_required('alias', alias)
    if err:
        return err
    return xl.assign_alias(brick, alias)


@xw.func
@xw.arg('functions', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
@_return_errors
def xlb_create_function(functions, persist=True, xlapp=None):
    err = _check_array_2d('functions', functions)
    if err:
        return err
    return xl.create_function_objects(functions, persist, xlapp)


@xw.func
@xw.arg('context_name')
@xw.arg('context_path')
@xw.arg('args', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
@_return_errors
def xlb_create_context(context_name, context_path, args=None, persist=True, xlapp=None):
    err = _check_required('context_name', context_name) or _check_required('context_path', context_path)
    if err:
        return err
    return xl.create_context_object(context_name, context_path, args, persist, xlapp)


@xw.func
@xw.arg('function_brick', np.array, ndim=2)
@xw.arg('function_name')
@xw.arg('args', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
@_return_errors
def xlb_run_function(function_brick, function_name, args=None, persist=True, xlapp=None):
    err = _check_array_2d('function_brick', function_brick) or _check_required('function_name', function_name)
    if err:
        return err
    return xl.run_function(function_brick, function_name, args, persist, xlapp)


@xw.func
@xw.arg('quantlib_object', np.array, ndim=2)
@xw.arg('function_name')
@xw.arg('args', np.array, ndim=2)
@xw.arg('xl_app', vba='Application')
@_return_errors
def xlb_run_quantlib_function(quantlib_object, function_name, args=None, persist=True, xl_app=None):
    err = _check_array_2d('quantlib_object', quantlib_object) or _check_required('function_name', function_name)
    if err:
        return err
    return xl.run_quantlib_function(quantlib_object, function_name, args, persist, xl_app)


@xw.func
@xw.arg('brick_1', np.array, ndim=2)
@xw.arg('brick_2', np.array, ndim=2)
@xw.arg('brick_3', np.array, ndim=2)
@xw.arg('brick_4', np.array, ndim=2)
@xw.arg('brick_5', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
@_return_errors
def xlb_merge(brick_1, brick_2, brick_3=None, brick_4=None, brick_5=None, persist=True, xlapp=None):
    err = _check_array_2d('brick_1', brick_1) or _check_array_2d('brick_2', brick_2)
    if err:
        return err
    return xl.merge_elements(brick_1, brick_2, brick_3, brick_4, brick_5, persist, xlapp)


@xw.func
@_return_errors
def xlb_today():
    return datetime.today()


@xw.func
@_return_errors
def xlb_clear_bricks_front():
    return xl.clear_bricks_front()


@xw.func
@_return_errors
def xlb_open_bricks_explorer():
    explorer_app = QApplication(sys.argv)
    img_path = _get_image_path('stars.png')
    explorer_app.setWindowIcon(QIcon(img_path))
    model = DictionaryTreeModel(node_structure_from_dict(XLBricksFrontStack().to_dict()))
    wizard = Explorer(model)
    wizard.display()
    sys.exit(explorer_app.exec_())


@xw.func
@xw.arg('data', np.array, ndim=2)
@_return_errors
def xlb_open_brick_explorer(data):
    err = _check_array_2d('data', data)
    if err:
        return err
    if XLUtils.is_bricks_front_name(data):
        key = ''.join(data[0, 0].split(':')[:-1])
        element = XLUtils.get_bricks(data)
        explorer_app = QApplication(sys.argv)
        img_path = _get_image_path('stars.png')
        explorer_app.setWindowIcon(QIcon(img_path))
        model = DictionaryTreeModel(node_structure_from_dict({key: element.to_dict()}))
        wizard = Explorer(model)
        wizard.display_one_element()
        sys.exit(explorer_app.exec_())


@xw.func
@_return_errors
def xlb_open_config_editor():
    """Open the XLBricks config editor UI (same as XLBricks Wizard, from Excel)."""
    config_app = QApplication(sys.argv)
    img_path = _get_image_path('settings.png')
    config_app.setWindowIcon(QIcon(img_path))
    show_config_editor()
    sys.exit(0)


def _get_package_dir():
    """Return the absolute path to the xlbricks package directory (where xlbfunctions.py lives)."""
    this_file = getattr(sys.modules[__name__], '__file__', None)
    if not this_file:
        return ''
    return osp.abspath(osp.dirname(this_file))


def _get_image_path(name: str):
    """Return path to an icon from the imgs folder. Works when run from Excel (uses absolute path)."""
    pkg_dir = _get_package_dir()
    if not pkg_dir:
        return ''
    imgs_dir = osp.join(pkg_dir, 'imgs')
    path = osp.join(imgs_dir, name)
    if osp.isfile(path):
        return path
    return ''


if __name__ == '__main__':
    xw.serve()
