from doublespinboxdelegate import DoubleSpinBoxDelegate
from productcatalogmodel import ProductCatalogModel
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableView, QMessageBox
from PyQt5.QtCore import Qt, QSortFilterProxyModel


class DlgProductCatalog(QDialog):

    def __init__(self, parent=None, domainModel=None, uiFacade=None):
        super(DlgProductCatalog, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("dlgproductcatalog.ui", self)

        # init instances
        self._domainModel = domainModel
        self._uiFacade = uiFacade

        # data members

        # table models
        self._productModel = ProductCatalogModel(self, self._domainModel)
        self._searchProxyModel = QSortFilterProxyModel(self)

        self.initDialog()

    def initDialog(self):
        # init widgets
        self.ui.tableProduct: QTableView
        self.ui.tableProduct.setItemDelegateForColumn(1, DoubleSpinBoxDelegate(parent=self.ui.tableProduct))

        # setup model
        self._searchProxyModel.setSourceModel(self._productModel)
        self.ui.tableProduct.setModel(self._searchProxyModel)
        # self._productModel.initModel()

        # setup signals
        self.ui.btnAddProduct.clicked.connect(self.onBtnAddProduct)
        self.ui.btnDeleteProduct.clicked.connect(self.onBtnDeleteProduct)

        # adjust UI
        self.ui.tableProduct.resizeColumnsToContents()

    def onBtnAddProduct(self):
        self._productModel.addProduct()

    def onBtnDeleteProduct(self):
        if not self.ui.tableProduct.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка!", "Выберите запись о приборе для удаления.")
            return False

        row = self.ui.tableProduct.selectionModel().selectedIndexes()[0].row()
        self._productModel.removeProduct(row)
