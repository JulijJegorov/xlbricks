from PyQt5 import QtCore
import pandas as pd
import numpy as np


class PandasModel(QtCore.QAbstractTableModel):

    def __init__(self, df=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                try:
                    return self._df.columns.tolist()[section]
                except (IndexError, ):
                    return QtCore.QVariant()
            elif orientation == QtCore.Qt.Vertical:
                try:
                    return self._df.index.tolist()[section]
                except (IndexError, ):
                    return QtCore.QVariant()
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.QVariant(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        elif role == QtCore.Qt.SizeHintRole:
            pass
        return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            self._df.index = self._df.index.map(str)
            cell_value = self._df.iloc[index.row(), index.column()]
            if isinstance(cell_value, np.float):
                cell_value = np.around(cell_value, 5)
                return QtCore.QVariant(str(cell_value))
            return QtCore.QVariant(str(cell_value))

        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.QVariant(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        return QtCore.QVariant()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

