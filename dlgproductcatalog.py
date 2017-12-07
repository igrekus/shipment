from doublespinboxdelegate import DoubleSpinBoxDelegate
from inputdialog import InputDialog
from productcatalogmodel import ProductCatalogModel
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableView, QMessageBox, QLineEdit, QDoubleSpinBox
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex, QItemSelectionModel


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

        # setup signals
        self.ui.btnAddProduct.clicked.connect(self.onBtnAddProduct)
        self.ui.btnEditProduct.clicked.connect(self.onBtnEditProduct)
        self.ui.btnDeleteProduct.clicked.connect(self.onBtnDeleteProduct)

        # adjust UI
        self.ui.tableProduct.resizeColumnsToContents()

    def onBtnAddProduct(self):
        dialog = InputDialog(parent=self, title="Введите информацию о приборе",
                             widgetList=[QLineEdit, QDoubleSpinBox],
                             widgetTitleList=["Название: ", "Цена, руб.: "],
                             widgetDataList=["Новый прибор", 0.0])
        if dialog.exec() != QDialog.Accepted:
            return

        data = dialog.getData()
        self._domainModel.addProduct(data[0], int(data[1]*100))

        self.ui.tableProduct.scrollToBottom()

    def onBtnEditProduct(self):
        print("edit product")

    def onBtnDeleteProduct(self):
        if not self.ui.tableProduct.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка!", "Выберите запись о приборе для удаления.")
            return False

        row = self.ui.tableProduct.selectionModel().selectedIndexes()[0].row()
        self._productModel.removeProduct(row)
