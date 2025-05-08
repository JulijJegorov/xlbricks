"""
    Author: julij
    Date: 05/10/2022
    Description: 
"""

import sys
import os.path as osp
import numpy as np
import xlwings as xw
from datetime import datetime
import xlbricks.libs.xlfunctions as xl
from xlbricks.libs.utility_functions import XLUtils

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from xlbricks.ui.explorer import Explorer
from xlbricks.ui.tree_model import DictionaryTreeModel, node_structure_from_dict
from xlbricks.libs.xlbricks_frontstack import XLBricksFrontStack


@xw.func
@xw.arg('data', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
def xlb_brick(key, data, persist=True, xlapp=None):
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
def xlb_bricks(key_1, brick_1, key_2=None, brick_2=None, key_3=None, brick_3=None,
               key_4=None, brick_4=None, key_5=None, brick_5=None, key_6=None, brick_6=None,
               key_7=None, brick_7=None, key_8=None, brick_8=None, persist=True, xlapp=None):
    return xl.xlbricks_create(key_1, brick_1, key_2, brick_2, key_3, brick_3, key_4, brick_4,
                              key_5, brick_5, key_6, brick_6, key_7, brick_7, key_8, brick_8, persist, xlapp)


@xw.func
@xw.arg('data', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
def xlb_array(data, persist=True, xlapp=None):
    return xl.array_create(data, persist, xlapp)


@xw.func
@xw.arg('data', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
def xlb_list(data, persist=True, xlapp=None):
    return xl.list_create(data, persist, xlapp)


@xw.func
@xw.arg('data', np.array, ndim=2)
@xw.arg('index', np.array, ndim=2)
@xw.arg('columns', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
def xlb_table(data, columns=None, index=None, persist=True, xlapp=None):
    return xl.table_create(data, columns, index, persist, xlapp)


@xw.func
@xw.arg('data', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
def xlb_grid(data, persist=True, xlapp=None):
    return xl.grid_create(data, persist, xlapp)


@xw.func
@xw.arg('bricks', np.array, ndim=2)
@xw.arg('keys')
@xw.arg('xlapp', vba='Application')
def xlb_lookup(bricks, keys=None, persist=True, xlapp=None):
    return xl.lookup_element(bricks, keys, persist, xlapp)


@xw.func
@xw.arg('brick', np.array, ndim=2)
def xlb_flatten(brick):
    return xl.flatten_element(brick)


@xw.func
@xw.arg('brick', np.array, ndim=2)
def xlb_alias(brick, alias):
    return xl.assign_alias(brick, alias)


@xw.func
@xw.arg('functions', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
def xlb_create_function(functions, persist=True, xlapp=None):
    return xl.create_function_objects(functions, persist, xlapp)


@xw.func
@xw.arg('context_name')
@xw.arg('context_path')
@xw.arg('args', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
def xlb_create_context(context_name, context_path, args=None, persist=True, xlapp=None):
    return xl.create_context_object(context_name, context_path, args, persist, xlapp)


@xw.func
@xw.arg('function_brick', np.array, ndim=2)
@xw.arg('function_name')
@xw.arg('args', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
def xlb_run_function(function_brick, function_name, args=None, persist=True, xlapp=None):
    return xl.run_function(function_brick, function_name, args, persist, xlapp)


@xw.func
@xw.arg('quantlib_object', np.array, ndim=2)
@xw.arg('function_name')
@xw.arg('args', np.array, ndim=2)
@xw.arg('xl_app', vba='Application')
def xlb_run_quantlib_function(quantlib_object, function_name, args=None, persist=True, xl_app=None):
    return xl.run_quantlib_function(quantlib_object, function_name, args, persist, xl_app)


@xw.func
@xw.arg('brick_1', np.array, ndim=2)
@xw.arg('brick_2', np.array, ndim=2)
@xw.arg('brick_3', np.array, ndim=2)
@xw.arg('brick_4', np.array, ndim=2)
@xw.arg('brick_5', np.array, ndim=2)
@xw.arg('xlapp', vba='Application')
def xlb_merge(brick_1, brick_2, brick_3=None, brick_4=None, brick_5=None, persist=True, xlapp=None):
    return xl.merge_elements(brick_1, brick_2, brick_3, brick_4, brick_5, persist, xlapp)


@xw.func
def xlb_today():
    return datetime.today()


@xw.func
def xlb_clear_bricks_front():
    return xl.clear_bricks_front()


@xw.func
def xlb_open_bricks_explorer():
    explorer_app = QApplication(sys.argv)
    img_path = _get_wizard_image_path()
    explorer_app.setWindowIcon((QIcon(img_path)))
    model = DictionaryTreeModel(node_structure_from_dict(XLBricksFrontStack().to_dict()))
    wizard = Explorer(model)
    wizard.display()
    sys.exit(explorer_app.exec_())


@xw.func
@xw.arg('data', np.array, ndim=2)
def xlb_open_brick_explorer(data):
    if XLUtils.is_bricks_front_name(data):
        key = ''.join(data[0, 0].split(':')[:-1])
        element = XLUtils.get_bricks(data)
        explorer_app = QApplication(sys.argv)
        img_path = _get_wizard_image_path()
        explorer_app.setWindowIcon((QIcon(img_path)))
        model = DictionaryTreeModel(node_structure_from_dict({key: element.to_dict()}))
        wizard = Explorer(model)
        wizard.display_one_element()
        sys.exit(explorer_app.exec_())


def _get_wizard_image_path():
    return osp.join(osp.dirname(sys.modules[__name__].__file__), 'img/wizard.png')


if __name__ == '__main__':
    xw.serve()
