import const
import datetime
import isoweek
from domainmodel import DomainModel
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, QDate, pyqtSlot
from PyQt5.QtGui import QBrush, QColor


class ProductListModel(QAbstractTableModel):
    ColumnName = 0
    ColumnAmount = ColumnName + 1
    ColumnCount = ColumnAmount + 1

    _header = ["Наименование", "Кол-во (шт.)"]

    def __init__(self, parent=None, domainModel=None):
        super(ProductListModel, self).__init__(parent)

        self._modelDomain: DomainModel = domainModel
        self._productList = list()

    def clear(self):
        self.beginResetModel()
        self._productList.clear()
        self.endResetModel()

    def initModel(self, products: list):
        print("init product list model")
        if products is None:
            return
        count = len(products) - 1
        if count < 0:
            count = 0
        self.beginInsertRows(QModelIndex(), 0, count)
        self._productList = products
        self.endInsertRows()

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(self._header):
            return QVariant(self._header[section])
        return QVariant()

    def rowCount(self, parent=QModelIndex(), *args, **kwargs):
        if parent.isValid():
            return 0
        return len(self._productList)

    def columnCount(self, parent=None, *args, **kwargs):
        return self.ColumnCount

    def setData(self, index, value, role=None):
        col = index.column()
        row = index.row()

        if role == Qt.EditRole:
            if col == self.ColumnName:
                self._productList[row][1] = value
            elif col == self.ColumnAmount:
                self._productList[row][2] = value

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()

        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            if col == self.ColumnName:
                return QVariant(self._modelDomain.productMapModel.getData(self._productList[row][1]))
            elif col == self.ColumnAmount:
                return QVariant(str(self._productList[row][2]) + " шт.")

        if role == Qt.EditRole:
            if col == self.ColumnName:
                return QVariant(self._productList[row][1])
            elif col == self.ColumnAmount:
                return QVariant(self._productList[row][2])

        # elif role == Qt.BackgroundRole:
        #     return QVariant()

        elif role == const.RoleNodeId:
            return QVariant(self._productList[row][0])

        elif role == const.RoleProduct:
            return QVariant(self._productList[row][1])

        return QVariant()

    def flags(self, index):
        f = super(ProductListModel, self).flags(index)
        return f | Qt.ItemIsEditable

    def addProduct(self, id_):
        self.beginInsertRows(QModelIndex(), len(self._productList), len(self._productList))
        self._productList.append([0, id_, 0])
        self.endInsertRows()

    def removeProduct(self, row: int):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._productList[row]
        self.endRemoveRows()
    # @pyqtSlot(int, int)
    # def planItemsBeginInsert(self, first: int, last: int):
    #     self.beginInsertRows(QModelIndex(), first, last)
    #
    # @pyqtSlot()
    # def planItemsEndInsert(self):
    #     self.endInsertRows()
    #
    # @pyqtSlot(int, int)
    # def planItemsBeginRemove(self, first: int, last: int):
    #     self.beginRemoveRows(QModelIndex(), first, last)
    #
    # @pyqtSlot()
    # def planItemsEndRemove(self):
    #     self.endRemoveRows()
