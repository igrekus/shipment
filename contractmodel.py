import const
from PyQt5.QtCore import Qt, QModelIndex, QVariant, QDate, pyqtSlot, pyqtSignal, QAbstractItemModel

from contractitem import ContractItem


class TreeNode(object):

    def __init__(self, data=None, parent=None):
        self.data = data
        self.parentNode = parent
        self.childNodes = list()

    def appendChild(self, item):
        self.childNodes.append(item)

    def child(self, row):
        return self.childNodes[row]

    def childCount(self):
        return len(self.childNodes)

    def parent(self):
        return self.parentNode

    def row(self):
        if self.parentNode:
            return self.parentNode.childItems.index(self)
        return 0

    def __str__(self):
        return "TreeNode(data:" + str(self.data) + " parent:" + str(id(self.parentNode)) + " children:" + str(
            len(self.childNodes)) + ")"

class ContractModel(QAbstractItemModel):

    ColumnId = 0
    ColumnIndex = ColumnId + 1
    ColumnClient = ColumnIndex + 1
    ColumnCount = ColumnClient + 1

    _headers = ["id", "index", "client"]

    def __init__(self, parent=None, domainModel=None):
        super(ContractModel, self).__init__(parent)
        self._modelDomain = domainModel

        self.rootNode = TreeNode(None, None)

        self._modelDomain.contractAdded.connect(self.contractAdded)
        self._modelDomain.contractUpdated.connect(self.contractUpdated)
        self._modelDomain.contractRemoved.connect(self.contractRemoved)

    def clear(self):
        def clearTreeNode(node):
            if node.childNodes:
                for n in node.childNodes:
                    clearTreeNode(n)
            node.childNodes.clear()

        clearTreeNode(self.rootNode)

    def buildFirstLevel(self, data):
        for k, v in data.items():
            self.rootNode.appendChild(TreeNode(k, self.rootNode))

    # def buildSecondLevel(self, mapping):
    #     for n in self.rootNode.childNodes:
    #         for i in mapping[n.data]:
    #             n.appendChild(TreeNode(self._modelDomain.getItemById(i).item_id, n))
    #
    def buildTree(self):
        self.buildFirstLevel(data=self._modelDomain.contractList)
        # self.buildSecondLevel(mapping=self._modelDomain.substMap)

    def initModel(self):
        print("init tree model")
        self.beginResetModel()
        self.clear()
        self.rootNode = TreeNode(None, None)
        self.buildTree()
        self.endResetModel()

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(self._headers):
            return QVariant(self._headers[section])
        return QVariant()

    def rowCount(self, parent=QModelIndex(), *args, **kwargs):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentNode = self.rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    def columnCount(self, parent=QModelIndex(), *args, **kwargs):
        return self.ColumnCount

    def index(self, row, col, parent, *args, **kwargs):

        if not self.hasIndex(row, col, parent):
            return QModelIndex()

        if not parent.isValid():
            parentNode = self.rootNode
        else:
            parentNode = parent.internalPointer()

        childNode = parentNode.child(row)
        if childNode:
            return self.createIndex(row, col, childNode)
        else:
            return QModelIndex()

    def parent(self, index):

        if not index.isValid():
            return QModelIndex()

        childNode = index.internalPointer()
        if not childNode:
            return QModelIndex()

        parentNode = childNode.parent()

        if parentNode == self.rootNode:
            return QModelIndex()

        return self.createIndex(parentNode.row(), index.column(), parentNode)

    # def setData(self, index, value, role):
    #     return True

    def data(self, index: QModelIndex, role=None):
        if not index.isValid():
            return QVariant()

        col = index.column()

        item: ContractItem = self._modelDomain.getItemById(index.internalPointer().data)

        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            if col == self.ColumnId:
                return QVariant(item.item_id)
            elif col == self.ColumnIndex:
                return QVariant(item.item_index)
            elif col == self.ColumnClient:
                return QVariant(item.item_clientRef)

        # elif role == Qt.BackgroundRole:
        #     retcolor = Qt.white;
        #
        #     if item.item_status == 1:
        #         retcolor = const.COLOR_PAYMENT_FINISHED
        #
        #     if col == self.ColumnStatus:
        #         if item.item_status == 2:
        #             retcolor = const.COLOR_PAYMENT_PENDING
        #     if col == self.ColumnPriority:
        #         if item.item_status != 1:
        #             if item.item_priority == 2:  # 3 4
        #                 retcolor = const.COLOR_PRIORITY_LOW
        #             elif item.item_priority == 3:
        #                 retcolor = const.COLOR_PRIORITY_MEDIUM
        #             elif item.item_priority == 4:
        #                 retcolor = const.COLOR_PRIORITY_HIGH
        #     if col == self.ColumnShipmentStatus:
        #         if item.item_shipment_status == 2:
        #             retcolor = const.COLOR_ARRIVAL_PENDING
        #         if item.item_shipment_status == 3:
        #             retcolor = const.COLOR_ARRIVAL_PARTIAL
        #         if item.item_shipment_status == 4:
        #             retcolor = const.COLOR_ARRIVAL_RECLAIM
        #     return QVariant(QBrush(QColor(retcolor)))

        elif role == const.RoleNodeId:
            return QVariant(item.item_id)

        elif role == const.RoleClient:
            return QVariant(item.item_clientRef)

        return QVariant()

    # def flags(self, index):
    #     f = super(DeviceListModel, self).flags(index)
    #     return f

    @pyqtSlot(int)
    def contractAdded(self, newId: int):
        # TODO: if performance issues -- don't rebuild the whole tree, just add inserted item
        print("device added slot:", newId, self._treeType)
        self.initModel()

    @pyqtSlot(int)
    def contractUpdated(self, devId: int):
        print("device updated slot:", devId)
        self.treeType = self._treeType

    @pyqtSlot(int)
    def contractRemoved(self, devId: int):
        print("device removed slot:", devId)
        self.treeType = self._treeType

    # @property
    # def treeType(self):
    #     return self._treeType
    #
    # @treeType.setter
    # def treeType(self, treetype: int):
    #     self._treeType = treetype
    #     self.initModel()

    # @pyqtSlot(int, int)
    # def itemsInserted(self, first: int, last: int):
    #     self.beginInsertRows(QModelIndex(), first, last)
    #     # print("table model slot:", first, last)
    #     self.endInsertRows()
    #
    # @pyqtSlot(int, int)
    # def itemsRemoved(self, first: int, last: int):
    #     self.beginRemoveRows(QModelIndex(), first, last)
    #     # print("table model slot:", first, last)
    #     self.endRemoveRows()
