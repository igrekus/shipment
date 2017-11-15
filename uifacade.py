from functools import reduce

import const
from PyQt5.QtCore import QObject, QModelIndex, Qt
from PyQt5.QtWidgets import QDialog, QMessageBox

from contractitem import ContractItem
from dlgcontractdata import DlgContractData


class UiFacade(QObject):

    def __init__(self, parent=None, domainModel=None, reportManager=None):
        super(UiFacade, self).__init__(parent)
        self._domainModel = domainModel
        self._reportManager = reportManager

    def setDomainModel(self, domainModel=None):
        self._domainModel = domainModel

    def initFacade(self):
        print("init ui facade")

    # process ui requests
    # def requestRefresh(self):
    #     self._domainModel.refreshData()
    #     print("ui facade refresh request")
    #
    # def requestItemInfo(self, index: QModelIndex):
    #     item: DeviceItem = self._domainModel.getItemById(index.data(const.RoleNodeId))
    #     return "Наименование:\n" + item.item_name + \
    #            "\n\nПроизводитель:\n" + self._domainModel.getVendorById(item.item_vendor)[0] + \
    #            "\n\nТип устройства:\n" + self._domainModel.getDevtypeById(item.item_devtype) + \
    #            "\n\nОписание:\n" + item.item_desc + \
    #            "\n\nПараметры:\n" + item.item_spec

    def findDiffBetweenProductLists(self, old: list, new: list):
        added = list()
        changed = list()
        deleted = list()

        for n in new:
            if n in old:
                continue
            elif any(o[0] == n[0] for o in old):
                changed.append(n)
            else:
                added.append(n)

        for o in old:
            if not any(n[0] == o[0] for n in new):
                deleted.append(o)

        return added, changed, deleted

    def requestContractAdd(self):
        print("ui facade add contract request")
        dialog = DlgContractData(domainModel=self._domainModel, item=None, products=None)  # empty dialog for a new item

        if dialog.exec() != QDialog.Accepted:
            return

        newItem, products = dialog.getData()

        self._domainModel.addContractItem(newItem, products)

    def requestContractEdit(self, index: QModelIndex):
        item: ContractItem = self._domainModel.getItemById(index.data(const.RoleNodeId))
        print("ui facade edit device request", item)

        oldProducts = self._domainModel.contractDetailList[item.item_id]

        dialog = DlgContractData(domainModel=self._domainModel, item=item,
                                 products=oldProducts)

        if dialog.exec() != QDialog.Accepted:
            return

        updatedItem, updatedProducts = dialog.getData()

        added, changed, deleted = self.findDiffBetweenProductLists(oldProducts, updatedProducts)

        print(oldProducts)
        print(updatedProducts)
        print(added)
        print(changed)
        print(deleted)
        self._domainModel.updateContractItem(item, updatedProducts, (added, changed, deleted))

    def requestContractDelete(self, index: QModelIndex):
        item = self._domainModel.getItemById(index.data(const.RoleNodeId))
        print("ui facade delete contract request", item)

        result = QMessageBox.question(self.parent(), "Внимание!",
                                      "Вы хотите удалить выбранную запись?")

        if result != QMessageBox.Yes:
            return

        self._domainModel.deleteContractItem(item)

    # def requestExit(self, index):
    #     # TODO make settings class if needed, only current week is saved for now
    #     print("ui facade exit request...")
    #     print("saving preferences...", index)
    #     # TODO extract saving process into settings class, only send a message from UI
    #     with open("settings.ini", mode='tw') as f:
    #         f.write("week="+str(index + 1))
    #
    #     if self._domainModel.savePlanData():
    #         print("...exit request ok")
    #     else:
    #         raise RuntimeError("DB connection error")
