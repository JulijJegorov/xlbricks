
import pandas as pd
from xlbricks.ui.node import Node
from PyQt5 import QtCore

class DictionaryTreeModel(QtCore.QAbstractItemModel):
    """Data model providing a tree of an arbitrary dictionary"""

    def __init__(self, root, parent=None):
        super(DictionaryTreeModel, self).__init__(parent)
        self._rootNode = root

    def rowCount(self, parent):
        """the number of rows is the number of children"""
        if not parent.isValid():
            parent_node = self._rootNode
        else:
            parent_node = parent.internalPointer()

        return parent_node.child_count()

    def columnCount(self, parent):
        """Number of columns is always 2 since dictionaries consist of key-value pairs"""
        return 1

    def data(self, index, role):
        """returns the data requested by the view"""
        if not index.isValid():
            return None

        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return node.data(index.column())

    def parent(self, index):
        """returns the parent from given index"""
        node = self.get_node(index)
        parent_node = node.parent()
        if parent_node == self._rootNode:
            return QtCore.QModelIndex()

        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column, parent):
        """returns an index from given row, column and parent"""
        parent_node = self.get_node(parent)
        child_item = parent_node.child(row)

        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QtCore.QModelIndex()

    def get_node(self, index):
        """returns a Node() from given index"""
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self._rootNode


def node_structure_from_dict(datadict, parent=None, root_node=None):
    """returns a hierarchical node structure required by the TreeModel"""
    if not parent:
        root_node = Node('Root')
        parent = root_node

    for name, data in datadict.items():
        node = Node(name, parent)
        node.name = str(name)
        if isinstance(data, dict):
            node_structure_from_dict(data, node, root_node)
        elif isinstance(data, pd.DataFrame):
            node.value = data.head(min(25, len(data)))
        else:
            node.value = data

    return root_node

