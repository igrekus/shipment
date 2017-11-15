from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QAction, QMessageBox, QTreeView
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex

# import const
# from devicesearchproxymodel import DeviceSearchProxyModel
from contractitem import ContractItem
from contractmodel import ContractModel
from domainmodel import DomainModel
from mysqlengine import MysqlEngine
from persistencefacade import PersistenceFacade
from uifacade import UiFacade


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("mainwindow.ui", self)

        # report manager
        # self._reportManager = ReportManager(parent=self)

        # report engines
        # self._xlsxEngine = XlsxEngine(parent=self)
        # self._reportManager.setEngine(self._xlsxEngine)
        # self._printEngine = PrintEngine(parent=self)
        # self._reportManager.setEngine(self._printEngine)

        # persistence engine
        self._persistenceEngine = MysqlEngine(parent=self, dbItemClass=ContractItem)

        # facades
        self._persistenceFacade = PersistenceFacade(parent=self, persistenceEngine=self._persistenceEngine)
        # self._uiFacade = UiFacade(parent=self, reportManager=self._reportManager)
        self._uiFacade = UiFacade(parent=self)

        # models
        # domain
        self._modelDomain = DomainModel(parent=self, persistenceFacade=self._persistenceFacade)

        # device tree + search proxy
        self._modelContractTree = ContractModel(parent=self, domainModel=self._modelDomain)
        self._modelSearchProxy = QSortFilterProxyModel(parent=self)
        # self._modelSearchProxy = DeviceSearchProxyModel(parent=self)
        self._modelSearchProxy.setSourceModel(self._modelContractTree)

        # connect ui facade to models
        self._uiFacade.setDomainModel(self._modelDomain)

        # actions
        self.actRefresh = QAction("Обновить", self)
        self.actContractAdd = QAction("Добавить поставку", self)
        self.actContractEdit = QAction("Изменить поставку", self)
        self.actContractDelete = QAction("Удалить поставку", self)

    def initApp(self):
        # init instances
        # engines
        self._persistenceEngine.initEngine()

        # facades
        self._persistenceFacade.initFacade()
        self._uiFacade.initFacade()

        # models
        self._modelDomain.initModel()
        self._modelContractTree.initModel()

        # init UI
        # main table
        self.ui.treeContract: QTreeView
        self.ui.treeContract.setModel(self._modelSearchProxy)
        self.ui.treeContract.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.treeContract.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.treeContract.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # formatting
        # self.ui.treeContract.setUniformRowHeights(True)
        self.ui.treeContract.header().setHighlightSections(False)
        self.ui.treeContract.header().setStretchLastSection(True)

        # setup filter widgets
        # self.ui.comboVendorFilter.setModel(self._modelDomain.vendorMapModel)
        # self.ui.comboDevtypeFilter.setModel(self._modelDomain.devtypeMapModel)

        # create actions
        self.initActions()

        # setup ui widget signals
        # buttons
        self.ui.btnContractAdd.clicked.connect(self.onBtnContractAddClicked)
        self.ui.btnContractEdit.clicked.connect(self.onBtnContractEditClicked)
        self.ui.btnContractDelete.clicked.connect(self.onBtnContractDeleteClicked)

        # tree and selection
        # self.ui.treeDeviceList.selectionModel().currentChanged.connect(self.onCurrentTreeItemChanged)
        self.ui.treeContract.doubleClicked.connect(self.onTreeContractDoubleClicked)

        # search widgets
        # self.ui.comboVendorFilter.currentIndexChanged.connect(self.setSearchFilter)
        # self.ui.comboDevtypeFilter.currentIndexChanged.connect(self.setSearchFilter)
        # self.ui.editSearch.textChanged.connect(self.setSearchFilter)

        # UI modifications
        # self.ui.btnDictEditor.setVisible(False)
        # self.setSearchFilter()

    def initActions(self):
        self.actRefresh.setShortcut("Ctrl+R")
        self.actRefresh.setStatusTip("Обновить данные")
        self.actRefresh.triggered.connect(self.procActRefresh)

        self.actContractAdd.setStatusTip("Добавить поставку")
        self.actContractAdd.triggered.connect(self.procActContractAdd)

        self.actContractEdit.setStatusTip("Изменить поставку")
        self.actContractEdit.triggered.connect(self.procActContractEdit)

        self.actContractDelete.setStatusTip("Удалить поставку")
        self.actContractDelete.triggered.connect(self.procActContractDelete)

    def refreshView(self):
        windowRect = self.geometry()
        # tdwidth = windowRect.width() - 50
        #
        # self.ui.treeDeviceList.setColumnWidth(0, tdwidth * 0.15)
        # self.ui.treeDeviceList.setColumnWidth(1, tdwidth * 0.05)
        # self.ui.treeDeviceList.setColumnWidth(2, tdwidth * 0.10)
        # self.ui.treeDeviceList.setColumnWidth(3, tdwidth * 0.10)
        # self.ui.treeDeviceList.setColumnWidth(4, tdwidth * 0.20)
        # self.ui.treeDeviceList.setColumnWidth(5, tdwidth * 0.25)
        # self.ui.treeDeviceList.setColumnWidth(6, tdwidth * 0.15)

    # def updateItemInfo(self, index):
    #     self.ui.textDeviceInfo.setPlainText(self._uiFacade.requestItemInfo(index))

    # ui events
    def onBtnContractAddClicked(self):
        self.actContractAdd.trigger()

    def onBtnContractEditClicked(self):
        self.actContractEdit.trigger()

    def onBtnContractDeleteClicked(self):
        self.actContractDelete.trigger()

    # def onCurrentTreeItemChanged(self, cur: QModelIndex, prev: QModelIndex):
    #     sourceIndex = self._modelSearchProxy.mapToSource(cur)
    #     self.updateItemInfo(sourceIndex)

    def onTreeContractDoubleClicked(self, index):
        # if index.column() != 0:
        self.actContractEdit.trigger()

    # def setSearchFilter(self, dummy=0):
    #     self._modelSearchProxy.filterString = self.ui.editSearch.text()
    #     self._modelSearchProxy.filterVendor = self.ui.comboVendorFilter.currentData(const.RoleNodeId)
    #     self._modelSearchProxy.filterDevtype = self.ui.comboDevtypeFilter.currentData(const.RoleNodeId)
    #
    #     self._modelSearchProxy.invalidate()
    #     # self.ui.treeDeviceList.setColumnHidden(5, True)

    # misc events
    def resizeEvent(self, event):
        self.actRefresh.trigger()

    # def closeEvent(self, *args, **kwargs):
    #     self._uiFacade.requestExit()
    #     super(MainWindow, self).closeEvent(*args, **kwargs)

    # action processing
    # send user commands to the ui facade: (command, parameters (indexes, etc.))
    def procActRefresh(self):
        # print("act refresh triggered")
        # self._uiFacade.requestRefresh()
        self.refreshView()

    def procActContractAdd(self):
        self._uiFacade.requestContractAdd()

    def procActContractEdit(self):
        if not self.ui.treeContract.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка!", "Выберите запись о контракте для редактирования.")
            return False

        selectedIndex = self.ui.treeContract.selectionModel().selectedIndexes()[0]
        self._uiFacade.requestContractEdit(self._modelSearchProxy.mapToSource(selectedIndex))

    def procActContractDelete(self):
        if not self.ui.treeContract.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка!", "Выберите запись о контракте для удаления.")
            return False

        selectedIndex = self.ui.treeContract.selectionModel().selectedIndexes()[0]
        self._uiFacade.requestContractDelete(self._modelSearchProxy.mapToSource(selectedIndex))

