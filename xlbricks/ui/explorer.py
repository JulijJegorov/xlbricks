import numpy as np
import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLineEdit, QTreeView, QTableView, QPushButton, QSplitter, QVBoxLayout, QMessageBox
from xlbricks.libs.xlbricks_frontstack import XLBricksFrontStack

from xlbricks.ui.pandas_model import PandasModel
from xlbricks.ui.tree_model import DictionaryTreeModel, node_structure_from_dict


class Singleton(object):
    """Singleton base class """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class ExplorerTreeView(QTreeView):

    keyPressedNavigation = QtCore.pyqtSignal()
    keyPressedRefresh = QtCore.pyqtSignal()

    def __init__(self, model):
        super(QTreeView, self).__init__()
        self.setHeaderHidden(True)
        self.setModel(model)

    def keyPressEvent(self, event):
            super().keyPressEvent(event)
            if event.key() == QtCore.Qt.Key_Return \
                                                or event.key() == QtCore.Qt.Key_Down \
                                    or event.key() == QtCore.Qt.Key_Up \
                                    or event.key() == QtCore.Qt.Key_Left \
                                    or event.key() == QtCore.Qt.Key_Right:
                self.keyPressedNavigation.emit()

            elif event.key() == QtCore.Qt.Key_F5:
                self.keyPressedRefresh.emit()

            else:
                super().keyPressEvent(event)

    def refresh(self):
        model = DictionaryTreeModel(node_structure_from_dict(XLBricksFrontStack().to_dict()))
        self.setModel(model)


class ExplorerTableView(QTableView):
    def __init__(self):
        super(QTableView, self).__init__()
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet("selection-background-color: rgb(210, 232, 255); font-size: 16px; text-align: right;")

    def refresh(self, data=None):
        if data is None:
            df = pd.DataFrame()
        elif isinstance(data, (pd.DataFrame, np.ndarray)):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame(np.array([data]))
        df = pd.DataFrame()
        self.setModel(PandasModel(df))


class Explorer(QWidget):

    def __init__(self, model):
        super(Explorer, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self._entry = QLineEdit()
        self._tree_view = ExplorerTreeView(model)
        self._table_view = ExplorerTableView()
        self._button = QPushButton()

    def refresh(self):
        self._tree_view.refresh()
        self._table_view.refresh()

    def load_data_frame(self):
        item = self._tree_view.selectedIndexes()[0]
        index = self._tree_view.currentIndex()
        data_frame = item.model().get_node(index).value
        self._table_view.refresh(data_frame)
        self._table_view.resizeRowsToContents()

    def display(self):
        self.setWindowTitle('wizard')
        self.setMinimumSize(600, 400)
        self._tree_view.clicked.connect(self.load_data_frame)
        self._tree_view.keyPressedNavigation.connect(self.load_data_frame)
        vertical_box = QVBoxLayout()
        splitter = QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self._tree_view)
        splitter.addWidget(self._table_view)
        splitter.setSizes([100, 200])
        vertical_box.addWidget(splitter)
        self.setLayout(vertical_box)
        self.show()

    def display_one_element(self):
        self.setWindowTitle('wizard')
        self.setMinimumSize(200, 300)
        self._tree_view.clicked.connect(self.load_data_frame)
        self._tree_view.keyPressedNavigation.connect(self.load_data_frame)
        vertical_box = QVBoxLayout()
        splitter = QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self._tree_view)
        splitter.addWidget(self._table_view)
        splitter.setSizes([100, 200])
        vertical_box.addWidget(splitter)
        self.setLayout(vertical_box)
        self.show()

