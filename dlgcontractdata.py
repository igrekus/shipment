import sys
import const
import datetime
from copy import deepcopy
from comboboxdelegate import ComboBoxDelegate
from contractitem import ContractItem
from dateeditdelegate import DateEditDelegate
from productlistmodel import ProductListModel
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableView
from PyQt5.QtCore import Qt, QDate, QModelIndex

from spinboxdelegate import SpinBoxDelegate


class DlgContractData(QDialog):

    def __init__(self, parent=None, domainModel=None, uifacade=None, item=None, products=None):
        super(DlgContractData, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("DlgContractData.ui", self)

        # init instances
        self._domainModel = domainModel
        self._uiFacade = uifacade

        # data members
        self._currentItem: ContractItem = item
        self.newItem = None
        self._productList = list()
        if products is not None:
            self._productList = deepcopy(products)

        self._productModel = ProductListModel(self, self._domainModel)

        self.initDialog()

    def initDialog(self):
        # init widgets
        self.ui.tableProduct: QTableView
        self.ui.tableProduct.setItemDelegateForColumn(0, ComboBoxDelegate(parent=self.ui.tableProduct,
                                                                          mapModel=self._domainModel.dicts[
                                                                              const.DICT_PRODUCT]))
        self.ui.tableProduct.setItemDelegateForColumn(1, SpinBoxDelegate(parent=self.ui.tableProduct))
        self.ui.tableProduct.setItemDelegateForColumn(3, DateEditDelegate(parent=self.ui.tableProduct))

        self.ui.comboClient.setModel(self._domainModel.dicts[const.DICT_CLIENT])
        self.ui.tableProduct.setModel(self._productModel)
        self._productModel.initModel(self._productList)

        # setup signals
        self.ui.btnOk.clicked.connect(self.onBtnOkClicked)
        self.ui.btnClientAdd.clicked.connect(self.onBtnClientAddClicked)
        self.ui.btnProductAdd.clicked.connect(self.onBtnProductAddClicked)
        self.ui.btnProductRemove.clicked.connect(self.onBtnProductRemoveClicked)
        self.ui.btnNewProduct.clicked.connect(self.onBtnNewProductClicked)

        # set widget data
        if self._currentItem is None:
            self.resetWidgets()
        else:
            self.updateWidgets()

        # adjust UI
        self.ui.tableProduct.resizeColumnsToContents()

    def updateWidgets(self):

        def formatDate(date: datetime.date):
            if isinstance(date, datetime.date):
                return QDate().fromString(date.isoformat(), "yyyy-MM-dd")
            else:
                return QDate().fromString("2000-01-01", "yyyy-MM-dd")

        self.ui.editIndex.setText(self._currentItem.item_index)
        self.ui.comboClient.setCurrentText(self._domainModel.dicts[const.DICT_CLIENT].getData(self._currentItem.item_clientRef))
        self.ui.editProject.setText(self._currentItem.item_projCode)
        self.ui.editRequestN.setText(self._currentItem.item_requestN)
        self.ui.dateRequest.setDate(formatDate(self._currentItem.item_requestDate))
        self.ui.editDogozN.setText(self._currentItem.item_dogozName)
        self.ui.dateRequest.setDate(formatDate(self._currentItem.item_requestDate))
        self.ui.dateDogoz.setDate(formatDate(self._currentItem.item_dogozDate))
        self.ui.editDevRequestN.setText(self._currentItem.item_deviceRequestN)
        self.ui.editDevRequestCode.setText(self._currentItem.item_deviceRequestCode)
        self.ui.editContractN.setText(self._currentItem.item_contractN)
        self.ui.dateContract.setDate(formatDate(self._currentItem.item_contractDate))
        self.ui.dateSpecReturn.setDate(formatDate(self._currentItem.item_specReturnDate))
        self.ui.spinSum.setValue(float(self._currentItem.item_sum)/100)
        self.ui.editBillN.setText(self._currentItem.item_billNumber)
        self.ui.dateBill.setDate(formatDate(self._currentItem.item_billDate))
        self.ui.dateMil.setDate(formatDate(self._currentItem.item_milDate))
        self.ui.dateAddLetter.setDate(formatDate(self._currentItem.item_addLetterDate))
        self.ui.dateResponse.setDate(formatDate(self._currentItem.item_responseDate))
        self.ui.editPaymentN.setText(self._currentItem.item_paymentOrderN)
        self.ui.datePayment.setDate(formatDate(self._currentItem.item_paymentDate))
        self.ui.dateMatPurchase.setDate(formatDate(self._currentItem.item_matPurchaseDate))
        self.ui.datePlanShip.setDate(formatDate(self._currentItem.item_planShipmentDate))
        self.ui.dateManufPlan.setDate(formatDate(self._currentItem.item_manufPlanDate))
        self.ui.spinShipPeriod.setValue(self._currentItem.item_shipmentPeriod)
        self.ui.editInvoiceN.setText(self._currentItem.item_invoiceN)
        self.ui.dateInvoice.setDate(formatDate(self._currentItem.item_invoiceDate))
        self.ui.editPacklistN.setText(self._currentItem.item_packingListN)
        self.ui.datePacklist.setDate(formatDate(self._currentItem.item_packingListDate))
        self.ui.editShipNote.setText(self._currentItem.item_shipNote)
        self.ui.dateShip.setDate(formatDate(self._currentItem.item_shipDate))
        self.ui.checkComplete.setChecked(bool(self._currentItem.item_completed))
        self.ui.textContact.setPlainText(self._currentItem.item_contacts)

    def resetWidgets(self):
        currentDate = QDate().currentDate()
        self.ui.editIndex.setText("")
        self.ui.comboClient.setCurrentIndex(0)
        self.ui.editProject.setText("")
        self.ui.editRequestN.setText("")
        self.ui.dateRequest.setDate(currentDate)
        self.ui.editDogozN.setText("")
        self.ui.dateDogoz.setDate(currentDate)
        self.ui.editDevRequestN.setText("")
        self.ui.editDevRequestCode.setText("")
        self.ui.editContractN.setText("")
        self.ui.dateContract.setDate(currentDate)
        self.ui.dateSpecReturn.setDate(currentDate)
        self.ui.spinSum.setValue(0)
        self.ui.editBillN.setText("")
        self.ui.dateBill.setDate(currentDate)
        self.ui.dateMil.setDate(currentDate)
        self.ui.dateAddLetter.setDate(currentDate)
        self.ui.dateResponse.setDate(currentDate)
        self.ui.editPaymentN.setText("")
        self.ui.datePayment.setDate(currentDate)
        self.ui.dateMatPurchase.setDate(currentDate)
        self.ui.datePlanShip.setDate(currentDate)
        self.ui.dateManufPlan.setDate(currentDate)
        self.ui.spinShipPeriod.setValue(180)
        self.ui.editInvoiceN.setText("")
        self.ui.dateInvoice.setDate(currentDate)
        self.ui.editPacklistN.setText("")
        self.ui.datePacklist.setDate(currentDate)
        self.ui.editShipNote.setText("")
        self.ui.dateShip.setDate(currentDate)
        self.ui.checkComplete.setChecked(False)
        self.ui.textContact.setPlainText("")

    def verifyInputData(self):

        if not self.ui.editIndex.text():
            QMessageBox.information(self, "Ошибка", "Введите индекс поставки.")
            return False

        if self.ui.comboClient.currentData(const.RoleNodeId) == 0:
            QMessageBox.information(self, "Ошибка", "Выберите клиента.")
            return False

        if not self.ui.editProject.text():
            QMessageBox.information(self, "Ошибка", "Введите код работы.")
            return False

        if not self.ui.editRequestN.text():
            QMessageBox.information(self, "Ошибка", "Введите номер запроса.")
            return False

        if not self.ui.editDogozN.text():
            QMessageBox.information(self, "Ошибка", "Введите номер ДОГОЗ.")
            return False

        if self.ui.spinSum.value() <= 0:
            QMessageBox.information(self, "Ошибка", "Введите сумму.")
            return False

        if self.ui.spinShipPeriod.value() <= 0:
            QMessageBox.information(self, "Ошибка", "Введите срок поставки.")
            return False

        if self._productModel.rowCount() == 0:
            QMessageBox.information(self, "Ошибка", "Добавьте товары в список.")
            return False
        else:
            ids = self._productModel.getProductIdList()
            if len(ids) > len(set(ids)):
                QMessageBox.information(self, "Ошибка", "Товары в списке не должны повторяться.")
                return False

            # TODO: move to the model
            for i in range(self._productModel.rowCount()):
                if self._productModel.data(self._productModel.index(i, 0, QModelIndex()), Qt.DisplayRole).value() == "Все":
                    # TODO: fix crash on message dismissal
                    QMessageBox.information(self, "Ошибка", "Выберите товар из списка.")
                    return False

            # TODO: reject dupes in product list
        return True

    def collectData(self):

        # def getDate(strdate):
        #     return str

        id_ = None
        if self._currentItem is not None:
            id_ = self._currentItem.item_id

        completed = False
        if self._currentItem is not None:
            completed = self._currentItem.item_completed

        # TODO: change date formats
        self.newItem = ContractItem(id_=id_,
                                    index=self.ui.editIndex.text(),
                                    clientRef=self.ui.comboClient.currentData(const.RoleNodeId),
                                    projCode=self.ui.editProject.text(),
                                    requestN=self.ui.editRequestN.text(),
                                    requestDate=datetime.datetime.strptime(
                                        self.ui.dateRequest.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    dogozName=self.ui.dateDogoz.text(),
                                    dogozDate=datetime.datetime.strptime(
                                        self.ui.dateDogoz.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    deviceRequestN=self.ui.editDevRequestN.text(),
                                    deviceRequestCode=self.ui.editDevRequestCode.text(),
                                    contractN=self.ui.editContractN.text(),
                                    contractDate=datetime.datetime.strptime(
                                        self.ui.dateContract.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    specReturnDate=datetime.datetime.strptime(
                                        self.ui.dateSpecReturn.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    sum=int(self.ui.spinSum.value() * 100),
                                    billNumber=self.ui.editBillN.text(),
                                    billDate=datetime.datetime.strptime(self.ui.dateBill.date().toString("yyyy-MM-dd"),
                                                                        "%Y-%m-%d").date(),
                                    milDate=datetime.datetime.strptime(self.ui.dateMil.date().toString("yyyy-MM-dd"),
                                                                       "%Y-%m-%d").date(),
                                    addLetterDate=datetime.datetime.strptime(
                                        self.ui.dateAddLetter.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    responseDate=datetime.datetime.strptime(
                                        self.ui.dateResponse.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    paymentOrderN=self.ui.editPaymentN.text(),
                                    paymentDate=datetime.datetime.strptime(
                                        self.ui.datePayment.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    matPurchaseDate=datetime.datetime.strptime(
                                        self.ui.dateMatPurchase.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    planShipmentDate=datetime.datetime.strptime(
                                        self.ui.datePlanShip.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    shipmentPeriod=self.ui.spinShipPeriod.value(),
                                    invoiceN=self.ui.editInvoiceN.text(),
                                    invoiceDate=datetime.datetime.strptime(
                                        self.ui.dateInvoice.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    packingListN=self.ui.editPacklistN.text(),
                                    packingListDate=datetime.datetime.strptime(
                                        self.ui.datePacklist.date().toString("yyyy-MM-dd"), "%Y-%m-%d").date(),
                                    shipNote=self.ui.editShipNote.text(),
                                    shipDate=datetime.datetime.strptime(self.ui.dateShip.date().toString("yyyy-MM-dd"),
                                                                        "%Y-%m-%d").date(),
                                    completed=completed,
                                    contacts=self.ui.textContact.toPlainText(),
                                    manufPlanDate=datetime.datetime.strptime(
                                        self.ui.dateManufPlan.date().toString("yyyy-MM-dd"), "%Y-%m-%d"))

        self._productList = self._productModel.getProductList()

    def getData(self):
        return self.newItem, self._productList

    def onBtnOkClicked(self):
        if not self.verifyInputData():
            return
        self.collectData()
        self.accept()

    def onBtnClientAddClicked(self):
        self._uiFacade.requestClientAdd(caller=self)

    def onBtnProductAddClicked(self):
        self._productModel.addProduct(self._domainModel.dicts[const.DICT_PRODUCT].getIdByIndex(1))

    def onBtnProductRemoveClicked(self):
        if not self.ui.tableProduct.selectionModel().hasSelection():
            return

        result = QMessageBox.question(self.parent(), "Внимание!",
                                      "Вы хотите удалить выбранную запись?")

        if result != QMessageBox.Yes:
            return

        self._productModel.removeProduct(self.ui.tableProduct.selectionModel().selectedIndexes()[0].row())

    def onBtnNewProductClicked(self):
        self._uiFacade.requestProductAdd(caller=self)
