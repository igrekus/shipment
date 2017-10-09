import const
import datetime
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
    ColumnShipYear = ColumnIndex + 1   # synthetic column
    ColumnClient = ColumnShipYear + 1
    ColumnProjectCode = ColumnClient + 1
    ColumnProduct = ColumnProjectCode + 1   # synthetic column
    ColumnRequestNum = ColumnProduct + 1
    ColumnRequestDate = ColumnRequestNum + 1
    ColumnDogozName = ColumnRequestDate + 1
    ColumnDogozDate = ColumnDogozName + 1
    ColumnDeviceRequestNum = ColumnDogozDate + 1
    ColumnDeviceRequestCode = ColumnDeviceRequestNum + 1
    ColumnContractNum = ColumnDeviceRequestCode + 1
    ColumnContractDate = ColumnContractNum + 1
    ColumnSpecReturnDate = ColumnContractDate + 1
    ColumnSum = ColumnSpecReturnDate + 1
    ColumnBillNum = ColumnSum + 1
    ColumnBillDate = ColumnBillNum + 1
    ColumnMilDate = ColumnBillDate + 1
    ColumnAddLetterDate = ColumnMilDate + 1
    ColumnResponseDate = ColumnAddLetterDate + 1
    ColumnPaymentOrderNum = ColumnResponseDate + 1
    ColumnPaymentDate = ColumnPaymentOrderNum + 1
    ColumnMatPurchaseDate = ColumnPaymentDate + 1
    ColumnMinShipDate = ColumnMatPurchaseDate + 1   # synthetic
    ColumnMaxShipDate = ColumnMinShipDate + 1   # synthetic
    ColumnPlanShipmentDate = ColumnMaxShipDate + 1
    ColumnShipmentPeriod = ColumnPlanShipmentDate + 1
    ColumnInvoiceNum = ColumnShipmentPeriod + 1
    ColumnInvoiceDate = ColumnInvoiceNum + 1
    ColumnPackingListNum = ColumnInvoiceDate + 1
    ColumnPackingListDate = ColumnPackingListNum + 1
    ColumnShipNote = ColumnPackingListDate + 1
    ColumnShipDate = ColumnShipNote + 1
    ColumnCompleted = ColumnShipDate + 1
    ColumnContacts = ColumnCompleted + 1
    ColumnTaskDays = ColumnContacts + 1
    ColumnSpecDays = ColumnTaskDays + 1
    ColumnMilDays = ColumnSpecDays + 1
    ColumnClientDays = ColumnMilDays + 1
    ColumnPaymentDays = ColumnClientDays + 1
    ColumnMiscData = ColumnPaymentDays + 1
    ColumnCount = ColumnMiscData + 1

    _headers = ["id", "index", "shipyear", "client", "projcode", "prod", "reqnum", "reqdate", "dogozname", "dogozdate",
                "devreqnum", "devreqcode", "connum", "condate", "specretdate", "sum", "billnum", "billdate", "mildate",
                "addletterdate", "responsedate", "paynum", "paydate", "matpurchdate", "mindate", "maxdate", "plandate",
                "shipperiod", "invoicenum", "invoicedate", "packlistnum", "packlistdate", "shipnote", "shipdate",
                "complete", "contacts", "taskd", "specd", "mild", "cliemntd", "payd", "misc"]

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

        def getColumnProduct(model, item: ContractItem):
            return "".join(
                [model.productMapModel.getData(r[1]) + "/" for r in model.contractDetailList[item.item_id]]).strip("/")

        def getColumnPaymentDays(item: ContractItem):
            if not isinstance(item.item_paymentDate, datetime.date) \
                    or not isinstance(item.item_billDate, datetime.date):
                return str("N/A")
            return str((item.item_billDate - item.item_paymentDate).days)

        def getColumnClientDays(item: ContractItem):
            if not isinstance(item.item_responseDate, datetime.date) \
                    or not isinstance(item.item_addLetterDate, datetime.date):
                return str("N/A")
            return str((item.item_responseDate - item.item_addLetterDate).days)

        def getColumnMilDays(item: ContractItem):
            if not isinstance(item.item_addLetterDate, datetime.date) \
                    or not isinstance(item.item_milDate, datetime.date):
                return str("N/A")
            return str((item.item_addLetterDate - item.item_milDate).days)

        def getColumnSpecDays(item: ContractItem):
            if not isinstance(item.item_milDate, datetime.date) \
                    or not isinstance(item.item_specReturnDate, datetime.date):
                return str("N/A")
            return str((item.item_milDate - item.item_specReturnDate).days)

        def getColumnTaskDays(item: ContractItem):
            if not isinstance(item.item_specReturnDate, datetime.date) \
                    or not isinstance(item.item_requestDate, datetime.date):
                return str("N/A")
            return str((item.item_specReturnDate - item.item_requestDate).days)

        if not index.isValid():
            return QVariant()

        col = index.column()

        item: ContractItem = self._modelDomain.getItemById(index.internalPointer().data)

        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            if col == self.ColumnId:
                return QVariant(item.item_id)
            elif col == self.ColumnIndex:
                return QVariant(item.item_index)
            elif col == self.ColumnShipYear:
                if not isinstance(item.item_paymentDate, datetime.date):
                    return QVariant("N/A")
                return QVariant((item.item_paymentDate + datetime.timedelta(days=89)).year)
            elif col == self.ColumnClient:
                return QVariant(self._modelDomain.clientMapModel.getData(item.item_clientRef))
            elif col == self.ColumnProjectCode:
                return QVariant(item.item_projCode)
            elif col == self.ColumnProduct:
                return QVariant(getColumnProduct(self._modelDomain, item))
            elif col == self.ColumnRequestNum:
                return QVariant(item.item_requestN)
            elif col == self.ColumnRequestDate:
                return QVariant(str(item.item_requestDate))   # TODO format all dates
            elif col == self.ColumnDogozName:
                return QVariant(item.item_dogozName)
            elif col == self.ColumnDogozDate:
                return QVariant(str(item.item_dogozDate))
            elif col == self.ColumnDeviceRequestNum:
                return QVariant(item.item_deviceRequestN)
            elif col == self.ColumnDeviceRequestCode:
                return QVariant(item.item_deviceRequestCode)
            elif col == self.ColumnContractNum:
                return QVariant(item.item_contractN)
            elif col == self.ColumnContractDate:
                return QVariant(str(item.item_contractDate))
            elif col == self.ColumnSpecReturnDate:
                return QVariant(str(item.item_specReturnDate))
            elif col == self.ColumnSum:
                return QVariant(item.item_sum)   # TODO format suf output
            elif col == self.ColumnBillNum:
                return QVariant(item.item_billNumber)
            elif col == self.ColumnBillDate:
                return QVariant(str(item.item_billDate))
            elif col == self.ColumnMilDate:
                return QVariant(str(item.item_milDate))
            elif col == self.ColumnAddLetterDate:
                return QVariant(str(item.item_addLetterDate))
            elif col == self.ColumnResponseDate:
                return QVariant(str(item.item_responseDate))
            elif col == self.ColumnPaymentOrderNum:
                return QVariant(item.item_paymentOrderN)
            elif col == self.ColumnPaymentDate:
                return QVariant(str(item.item_paymentDate))
            elif col == self.ColumnMatPurchaseDate:
                return QVariant(str(item.item_matPurchaseDate))
            elif col == self.ColumnMinShipDate:
                if not isinstance(item.item_paymentDate, datetime.date):
                    return QVariant("N/A")
                return QVariant(str(item.item_paymentDate + datetime.timedelta(days=89)))
            elif col == self.ColumnMaxShipDate:
                if not isinstance(item.item_paymentDate, datetime.date):
                    return QVariant("N/A")
                return QVariant(str(item.item_paymentDate + datetime.timedelta(days=item.item_shipmentPeriod - 1)))
            elif col == self.ColumnPlanShipmentDate:
                return QVariant(str(item.item_planShipmentDate))
            elif col == self.ColumnShipmentPeriod:
                return QVariant(item.item_shipmentPeriod)
            elif col == self.ColumnInvoiceNum:
                return QVariant(item.item_invoiceN)
            elif col == self.ColumnInvoiceDate:
                return QVariant(str(item.item_invoiceDate))
            elif col == self.ColumnPackingListNum:
                return QVariant(item.item_packingListN)
            elif col == self.ColumnPackingListDate:
                return QVariant(str(item.item_packingListDate))
            elif col == self.ColumnShipNote:
                return QVariant(item.item_shipNote)
            elif col == self.ColumnShipDate:
                return QVariant(str(item.item_shipDate))
            # elif col == self.ColumnCompleted:
            #     return QVariant(item.item_completed)
            elif col == self.ColumnContacts:
                return QVariant(item.item_contacts)
            elif col == self.ColumnTaskDays:
                return QVariant(getColumnTaskDays(item))
            elif col == self.ColumnSpecDays:
                return QVariant(getColumnSpecDays(item))
            elif col == self.ColumnMilDays:
                return QVariant(getColumnMilDays(item))
            elif col == self.ColumnClientDays:
                return QVariant(getColumnClientDays(item))
            elif col == self.ColumnPaymentDays:
                return QVariant(getColumnPaymentDays(item))
            elif col == self.ColumnMiscData:
                return QVariant("Заявка " + item.item_requestN +
                                " от " + str(item.item_requestDate) +
                                " на " + getColumnProduct(self._modelDomain, item))

        elif role == Qt.CheckStateRole:
            if col == self.ColumnCompleted:
                if item.item_completed == 0:
                    return QVariant(0)
                elif item.item_completed == 1:
                    return QVariant(2)

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

    # def flags(self, index: QModelIndex):
    #     f = super(DeviceListModel, self).flags(index)
    #     if index.column() == self.ColumnCompleted:
    #         f = f & Qt.ItemIsUserCheckable
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
