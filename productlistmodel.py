import datetime
import const
from domainmodel import DomainModel
from collections import defaultdict
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, QDate, pyqtSlot
from PyQt5.QtGui import QBrush, QColor


class ProductListModel(QAbstractTableModel):
    ColumnName = 0
    ColumnAmount = ColumnName + 1
    ColumnStatus = ColumnAmount + 1
    ColumnDoneDate = ColumnStatus + 1
    ColumnCount = ColumnDoneDate + 1

    _header = ["Наименование", "Кол-во (шт.)", "Статус", "Завершено"]

    def __init__(self, parent=None, domainModel=None):
        super(ProductListModel, self).__init__(parent)

        self._modelDomain: DomainModel = domainModel
        self._productList = list()

    def clear(self):
        self.beginResetModel()
        self._productList.clear()
        self.endResetModel()

    def initModel(self, products: list):
        # print("init product list model")
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

    def setData(self, index, value, role=None) -> bool:
        col = index.column()
        row = index.row()

        if role == Qt.EditRole:
            if col == self.ColumnName:
                self._productList[row][1] = value
                return True
            elif col == self.ColumnAmount:
                self._productList[row][2] = value
                return True
            elif col == self.ColumnDoneDate:
                self._productList[row][3] = datetime.datetime.strptime(value.toString("yyyy-MM-dd"), "%Y-%m-%d").date()
                return True

        elif role == Qt.CheckStateRole:
            if col == self.ColumnStatus:
                self._productList[row][4] = value/2
                self.dataChanged.emit(self.index(index.row(), self.ColumnCount, QModelIndex()),
                                      self.index(index.row(), self.ColumnCount, QModelIndex()), [])
                return True

        return False

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()

        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            if col == self.ColumnName:
                return QVariant(self._modelDomain.dicts[const.DICT_PRODUCT].getData(self._productList[row][1]))
            elif col == self.ColumnAmount:
                return QVariant(str(self._productList[row][2]) + " шт.")
            elif col == self.ColumnDoneDate:
                if self._productList[row][4] == 1:
                    return QVariant(self._productList[row][3].isoformat())
                else:
                    return QVariant("Ожидание")

        if role == Qt.EditRole:
            if col == self.ColumnName:
                return QVariant(self._productList[row][1])
            elif col == self.ColumnAmount:
                return QVariant(self._productList[row][2])
            elif col == self.ColumnDoneDate:
                return QVariant(QDate().fromString(self._productList[row][3].isoformat(), "yyyy-MM-dd"))

        # elif role == Qt.BackgroundRole:
        #     return QVariant()

        elif role == Qt.CheckStateRole:
            if col == self.ColumnStatus:
                return QVariant(self._productList[row][4] * 2)

        elif role == const.RoleNodeId:
            return QVariant(self._productList[row][0])

        elif role == const.RoleProduct:
            return QVariant(self._productList[row][1])

        return QVariant()

    def flags(self, index):
        f = super(ProductListModel, self).flags(index)
        if index.column() == self.ColumnStatus:
            return f | Qt.ItemIsUserCheckable
        if index.column() == self.ColumnDoneDate:
            if self._productList[index.row()][4] == 1:
                return f | Qt.ItemIsEditable
            else:
                return f
        return f | Qt.ItemIsEditable

    def getProductList(self) -> list:
        if not self._productList:
            return list()

        return self._productList

    def getProductIdList(self) -> list:
        return [p[1] for p in self._productList]

    def addProduct(self, id_):
        self.beginInsertRows(QModelIndex(), len(self._productList), len(self._productList))
        self._productList.append([0, id_, 0, datetime.date.today(), 0])
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
