"""
    Author: julij.jegorov
    Date: 15/02/2026
    Description: XLUtils (get_bricks, crop_range, etc.), XLBricksFunction decorator,
                 and XLBricksUtils; bridges Excel ranges to brick structures.
"""

import numpy as np
import pandas as pd
from xlbricks.libs.xlbricks import XLBrick, XLBricks
from xlbricks.libs.xlbricks_front import XLBricksFront
from xlbricks.libs.xlbricks_frontstack import XLBricksFrontStack, add_bricks_to_front_stack, delete_bricks_from_front_stack


class XLBricksFunction(object):
    """Decorator for xlfunctions: registers result in the front stack and returns brick reference."""

    def __init__(self, is_dynamic: bool = False):
        """Set is_dynamic: if True, return raw output when it is not an XLBricksFront."""
        self.is_dynamic = is_dynamic

    def __call__(self, f):
        """Wrap f: on success add result to front stack and return bricks_full_name (or raw if dynamic)."""
        def wrap(*args, **kwargs):
            xl_output = f(*args, **kwargs)
            if self.is_dynamic and not isinstance(xl_output, XLBricksFront):
                return xl_output

            add_bricks_to_front_stack(xl_output)
            return xl_output.bricks_full_name
        return wrap


class XLUtils(object):
    """Static helpers to convert Excel range data to bricks and manage the front stack."""

    @staticmethod
    def get_bricks_front(data):
        """Return the XLBricksFront for a 1x1 range containing a bricks reference (alias:counter), else None."""
        if XLUtils.is_bricks_front_name(data):
            key = ''.join(data[0, 0].split(':')[:-1])
            return XLBricksFrontStack()[key]
        else:
            return None

    @staticmethod
    def get_bricks(data):
        """Convert Excel range to XLBrick or XLBricks: crop empty edges, resolve references, coerce types."""
        data = XLUtils.crop_range(data)
        bricks_front = XLUtils.get_bricks_front(data)
        if bricks_front is None:
            if data.dtype.type is np.str_:
                data = pd.DataFrame(data).apply(pd.to_numeric, errors='ignore').values
            return XLBrick(None, data)
        else:
            delete_bricks_from_front_stack(bricks_front)
            return bricks_front.xlbricks

    @staticmethod
    def delete_bricks(data):
        """Remove the bricks front entry for the given 1x1 reference range (alias:counter)."""
        if XLUtils.is_bricks_front_name(data):
            key = ''.join(data[0, 0].split(':')[:-1])
            del XLBricksFrontStack()[key]

    @staticmethod
    def is_bricks_front_name(data):
        """Return True if data is a 1x1 cell containing a string with ':' (bricks reference)."""
        if data.shape == (1, 1) and isinstance(data[0, 0], str) and ':' in data[0, 0]:
            return True
        else:
            return False

    @staticmethod
    def crop_range(data):
        """Remove leading/trailing rows and columns that are entirely empty (nan/null)."""
        if data.dtype.type is np.str_:
            return XLUtils._crop_range(data, lambda x: x == 'nan')
        elif data.dtype.type is np.object_:
            return XLUtils._crop_range(data, lambda x: pd.isnull(x))
        else:
            return XLUtils._crop_range(data, lambda x: np.isnan(x))

    @staticmethod
    def _crop_range(data, func_isnan):
        """Strip fully empty rows/columns from all four sides using func_isnan to detect empty cells."""
        while func_isnan(data[0, :]).all():
            data = np.delete(data, 0, axis=0)

        while func_isnan(data[:, 0]).all():
            data = np.delete(data, 0, axis=1)

        rows, cols = data.shape
        row_idx = rows - 1
        while row_idx > 0 and func_isnan(data[row_idx, :]).all():
            data = np.delete(data, row_idx, axis=0)
            row_idx -= 1

        rows, cols = data.shape
        col_idx = cols - 1
        while col_idx > 0 and func_isnan(data[:, col_idx]).all():
            data = np.delete(data, col_idx, axis=1)
            col_idx -= 1

        return data

    @staticmethod
    def active_cell_address(xl_app):
        """Return full address of the calling cell as '[Workbook]Sheet!Address' (e.g. for persistence)."""
        active_cell = xl_app.Caller
        worksheet = active_cell.Parent
        workbook = worksheet.Parent
        address = '[%s]%s!%s' % (workbook.Name, worksheet.Name, active_cell.Address)
        return address


class XLBricksUtils(object):
    """Static helpers to build XLBricks/XLBrick from Python dicts and lists."""

    @staticmethod
    def element_from_dictionary(input_data):
        """Convert a nested dictionary to XLBricks; dict values become bricks, nested dicts recurse."""

        qd_element = XLBricks()
        for key, data in input_data.items():
            if isinstance(data, dict):
                qd_element[key] = XLBricksUtils.element_from_dictionary(data)
            else:
                qd_element[key] = XLBricks(None, data)

        return qd_element

    @staticmethod
    def element_from_list(input_data, key_prefix):
        """Convert a list to XLBricks with keys key_prefix_1, key_prefix_2, ..."""

        qd_element = XLBricks()
        for idx, res in enumerate(input_data, 1):
            qd_element['%s_%s' % (key_prefix, idx)] = XLBricks(None, res)

        return qd_element

