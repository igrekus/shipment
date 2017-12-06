import datetime
import const
from domainmodel import DomainModel
from collections import defaultdict
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, QDate, pyqtSlot
from PyQt5.QtGui import QBrush, QColor


class ProductCatalogModel(QAbstractTableModel):
    ColumnName = 0
    ColumnPrice = ColumnName + 1
    ColumnCount = ColumnPrice + 1

    _header = ["Наименование", "Цена"]

    def __init__(self, parent=None, domainModel=None):
        super(ProductCatalogModel, self).__init__(parent)

        self._modelDomain: DomainModel = domainModel
        self._productList = list()

        self.initModel()

    def clear(self):
        self.beginResetModel()
        self._productList.clear()
        self.endResetModel()

    def initModel(self):
        print("init product list model")
        # for k, v in self._modelDomain.dicts[const.DICT_PRODUCT].mapData.items():
        #     if k != 0:
        #         print(k, v, self._modelDomain.dicts[const.DICT_PRICE][k])

        self._productList = [[k, v, self._modelDomain.dicts[const.DICT_PRICE][k], const.ACTION_NO_ACTION] for k, v in
                             self._modelDomain.dicts[const.DICT_PRODUCT].mapData.items() if k != 0]

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
                if self._productList[row][1] == value:
                    return False
                self._productList[row][1] = value
                self._productList[row][3] = const.ACTION_MODIFY
                return True

            elif col == self.ColumnPrice:
                if self._productList[row][2] == int(value*100):
                    return False
                self._productList[row][2] = int(value*100)
                self._productList[row][3] = const.ACTION_MODIFY
                return True

        return False

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()
        item = self._productList[row]

        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            if col == self.ColumnName:
                return QVariant(item[1])
            elif col == self.ColumnPrice:
                return QVariant("{:,.2f}".format(float(item[2] / 100)).replace(",", " ")
                                .replace(".", ",") + " руб.")

        if role == Qt.EditRole:
            if col == self.ColumnName:
                return QVariant(item[1])
            elif col == self.ColumnPrice:
                return QVariant(float(item[2] / 100))

        # elif role == const.RoleNodeId:
        #     return QVariant(self._productList[row][0])
        #
        # elif role == const.RoleProduct:
        #     return QVariant(self._productList[row][1])

        return QVariant()

    def flags(self, index):
        f = super(ProductCatalogModel, self).flags(index)
        col = index.column()
        if col == self.ColumnName or col == self.ColumnPrice:
            return f | Qt.ItemIsEditable
        return f

    def getProductList(self) -> list:
        if not self._productList:
            return list()

        return self._productList

    def getProductIdList(self) -> list:
        return [p[1] for p in self._productList]

    def addProduct(self):
        self.beginInsertRows(QModelIndex(), len(self._productList), len(self._productList))
        self._productList.append([0, "Новый прибор", 0.0, const.ACTION_ADD])
        self.endInsertRows()

    def removeProduct(self, row: int):
        self.beginRemoveRows(QModelIndex(), row, row)
        self._productList[row][3] = const.ACTION_DELETE
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
