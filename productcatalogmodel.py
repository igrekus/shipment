import const
from domainmodel import DomainModel
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, pyqtSlot


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

        # connect signals
        self._modelDomain.productAdded.connect(self.productAdded)
        self._modelDomain.productRemoved.connect(self.productRemoved)
        self._modelDomain.productUpdated.connect(self.productUpdated)

    def clear(self):
        self.beginResetModel()
        self._productList.clear()
        self.endResetModel()

    def initModel(self):
        print("init product list model")
        self._productList = [[k, v, self._modelDomain.dicts[const.DICT_PRICE][k]] for k, v in
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
                return True

            elif col == self.ColumnPrice:
                if self._productList[row][2] == int(value*100):
                    return False
                self._productList[row][2] = int(value*100)
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

        elif role == const.RoleNodeId:
            return item[0]

        # elif role == const.RoleProduct:
        #     return QVariant(self._productList[row][1])

        return QVariant()

    # def flags(self, index):
    #     f = super(ProductCatalogModel, self).flags(index)
    #     col = index.column()
    #     if col == self.ColumnName or col == self.ColumnPrice:
    #         return f | Qt.ItemIsEditable
    #     return f

    def getProductList(self) -> list:
        if not self._productList:
            return list()

        return self._productList

    def addProduct(self, data: list):
        self.beginInsertRows(QModelIndex(), len(self._productList), len(self._productList))
        self._productList.append([0, "Новый прибор", 0.0])
        self.endInsertRows()
        return self.index(len(self._productList) - 1, 0, QModelIndex())

    def updateProduct(self, row: int, name: str, price: int):
        self._productList[row][1] = name
        self._productList[row][2] = price
        self.dataChanged.emit(self.index(row, 0, QModelIndex()), self.index(row, 2, QModelIndex()), [])

    def removeProduct(self, row: int):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._productList[row]
        self.endRemoveRows()

    @pyqtSlot(int)
    def productAdded(self, id_: int):
        # TODO: make proper insertion
        self.beginResetModel()
        self.clear()
        self.initModel()
        self.endResetModel()

    @pyqtSlot(int)
    def productUpdated(self, id_: int):
        pass

    @pyqtSlot(int)
    def productRemoved(self, id_: int):
        # TODO: make proper deletion
        self.beginResetModel()
        self.clear()
        self.initModel()
        self.endResetModel()

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
