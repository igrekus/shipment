import sys
import const
import datetime
from copy import copy
from comboboxdelegate import ComboBoxDelegate
from contractitem import ContractItem
from productlistmodel import ProductListModel
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableView
from PyQt5.QtCore import Qt, QDate

from spinboxdelegate import SpinBoxDelegate


class DlgContractData(QDialog):

    def __init__(self, parent=None, domainModel=None, item=None, products=None):
        super(DlgContractData, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("DlgContractData.ui", self)

        # init instances
        self._domainModel = domainModel

        # data members
        self._currentItem: ContractItem = item
        self.newItem = None
        self._productList = copy(products)
        self._productModel = ProductListModel(self, self._domainModel)

        self.initDialog()

    def initDialog(self):
        # init widgets
        self.ui.tableProduct: QTableView
        self.ui.tableProduct.setItemDelegateForColumn(0, ComboBoxDelegate(parent=self.ui.tableProduct,
                                                                          mapModel=self._domainModel.productMapModel))
        self.ui.tableProduct.setItemDelegateForColumn(1, SpinBoxDelegate(parent=self.ui.tableProduct))

        self.ui.comboClient.setModel(self._domainModel.clientMapModel)
        self.ui.tableProduct.setModel(self._productModel)
        self._productModel.initModel(self._productList)

        # setup signals
        self.ui.btnOk.clicked.connect(self.onBtnOkClicked)
        self.ui.btnClientAdd.clicked.connect(self.onBtnClientAddClicked)
        self.ui.btnProductAdd.clicked.connect(self.onBtnProductAddClicked)
        self.ui.btnProductRemove.clicked.connect(self.onBtnProductRemoveClicked)

        # set widget data
        if self._currentItem is None:
            self.resetWidgets()
        else:
            self.updateWidgets()

    def updateWidgets(self):

        def formatDate(date: datetime.date):
            if isinstance(date, datetime.date):
                return QDate().fromString(date.isoformat(), "yyyy-MM-dd")
            else:
                return QDate.currentDate()

        self.ui.editIndex.setText(self._currentItem.item_index)
        self.ui.comboClient.setCurrentText(self._domainModel.clientMapModel.getData(self._currentItem.item_clientRef))
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
        self.ui.dateSpectReturn.setDate(formatDate(self._currentItem.item_specReturnDate))
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
        self.ui.editIndex.setText("")
        self.ui.comboClient.setCurrentIndex(0)
        self.ui.editProject.setText("")
        self.ui.editRequestN.setText("")
        self.ui.dateRequest.setDate(QDate().currentDate())
        self.ui.editDogozN.setText("")
        self.ui.dateDogoz.setDate(QDate().currentDate())
        self.ui.editDevRequestN.setText("")
        self.ui.editDevRequestCode.setText("")
        self.ui.editContractN.setText("")
        self.ui.dateContract.setDate(QDate().currentDate())
        self.ui.dateSpectReturn.setDate(QDate().currentDate())
        self.ui.spinSum.setValue(0)
        self.ui.editBillN.setText("")
        self.ui.dateBill.setDate(QDate().currentDate())
        self.ui.dateMil.setDate(QDate().currentDate())
        self.ui.dateAddLetter.setDate(QDate().currentDate())
        self.ui.dateResponse.setDate(QDate().currentDate())
        self.ui.editPaymentN.setText("")
        self.ui.datePayment.setDate(QDate().currentDate())
        self.ui.dateMatPurchase.setDate(QDate().currentDate())
        self.ui.datePlanShip.setDate(QDate().currentDate())
        self.ui.dateManufPlan.setDate(QDate().currentDate())
        self.ui.spinShipPeriod.setValue(0)
        self.ui.editInvoiceN.setText("")
        self.ui.dateInvoice.setDate(QDate().currentDate())
        self.ui.editPacklistN.setText("")
        self.ui.datePacklist.setDate(QDate().currentDate())
        self.ui.editShipNote.setText("")
        self.ui.dateShip.setDate(QDate().currentDate())
        self.ui.checkComplete.setChecked(False)
        self.ui.textContact.setPlainText("")

    def verifyInputData(self):

        if not self.ui.editIndex.text():
            QMessageBox.information(self, "Ошибка", "Введите индекс поставки.")
            return False

        return True

    def collectData(self):
        pass
        # id_ = None
        # if self._currentItem is not None:
        #     id_ = self._currentItem.item_id

        # priority = self.ui.comboPriority.currentData(const.RoleNodeId)
        # if self.ui.comboStatus.currentData(const.RoleNodeId) == 1:
        #     priority = 1
        #
        # self.newItem = billitem.BillItem(id_=id_
        #                                  , date=self.ui.dateBill.date().toString("dd.MM.yyyy")
        #                                  , name=self.ui.editBillName.text()
        #                                  , category=self.ui.comboCategory.currentData(const.RoleNodeId)
        #                                  , vendor=self.ui.comboVendor.currentData(const.RoleNodeId)
        #                                  , cost=int(self.ui.spinCost.value()*100)
        #                                  , project=self.ui.comboProject.currentData(const.RoleNodeId)
        #                                  , descript=self.ui.textDescript.toPlainText()
        #                                  , shipment_time=self.ui.comboPeriod.currentData(const.RoleNodeId)
        #                                  , status=self.ui.comboStatus.currentData(const.RoleNodeId)
        #                                  , priority=priority
        #                                  , shipment_date=self.ui.dateShipment.date().toString("dd.MM.yyyy")
        #                                  , shipment_status=self.ui.comboShipment.currentData(const.RoleNodeId)
        #                                  , payment_week=self.ui.spinWeek.value()
        #                                  , note=self.ui.editNote.text())

        # TODO verify data change, reject dialog if not changed

    def getData(self):
        return self.newItem

    def onBtnOkClicked(self):
        if not self.verifyInputData():
            return

        self.collectData()
        self.accept()

    def onBtnClientAddClicked(self):
        print("add client")

    def onBtnProductAddClicked(self):
        print("add product:", self._domainModel.productMapModel.getIdByIndex(0))
        self._productModel.addRow(self._domainModel.productMapModel.getIdByIndex(0))

    def onBtnProductRemoveClicked(self):
        if not self.ui.tableProduct.selectionModel().hasSelection():
            return

        print("remove product:", self.ui.tableProduct.selectionModel().selectedIndexes()[0].row())
