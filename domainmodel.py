from collections import defaultdict
from contractitem import ContractItem
from mapmodel import MapModel
from PyQt5.QtCore import QObject, QModelIndex, pyqtSignal, QDate


class DomainModel(QObject):

    dict_list = ["client", "product"]

    contractAdded = pyqtSignal(int)
    contractUpdated = pyqtSignal(int)
    contractRemoved = pyqtSignal(int)

    def __init__(self, parent=None, persistenceFacade=None):
        super(DomainModel, self).__init__(parent)

        self._persistenceFacade = persistenceFacade

        self.contractList = dict()
        self.contractDetailList = dict()

        self.clientMapModel: MapModel = None
        self.productMapModel: MapModel = None

    def buildClientMapModel(self):
        self.clientMapModel = MapModel(self, self._persistenceFacade.getDict(self.dict_list[0]))

    def buildProductMapModel(self):
        self.productMapModel = MapModel(self, self._persistenceFacade.getDict(self.dict_list[1]))

    def initModel(self):
        print("init domain model")
        self.contractList = self._persistenceFacade.getContractList()
        self.contractDetailList = self._persistenceFacade.getContractDetailList()
        self.buildClientMapModel()
        self.clientMapModel.addItemAtPosition(0, 0, "Все")

        self.buildProductMapModel()
        self.productMapModel.addItemAtPosition(0, 0, "Все")

    def getItemById(self, id_):
        return self.contractList[id_]

    def addContractItem(self, item: ContractItem, products: list):
        print("domain model add contract item call:", item)
        print("products:", products)

        newItem, newDetaiList = self._persistenceFacade.insertContractItem(item, products)

        self.contractList[newItem.item_id] = newItem
        self.contractDetailList[newItem.item_id] = newDetaiList

        self.contractAdded.emit(newItem.item_id)

    def updateContractItem(self, item: ContractItem, products: list, updates: list):
        print("domain model update contract item call:", item)
        print("products", products)

        self.contractList[item.item_id] = item
        self.contractDetailList[item.item_id] = products

        self._persistenceFacade.updateContractItem(item, updates)

        self.contractUpdated.emit(item.item_id)

    def deleteContractItem(self, item: ContractItem):
        print("domain model delete contract item call:", item)
        print("deleting bound products")
        # self.deviceList.pop(item.item_id, 0)
        # self.substMap.pop(item.item_id, 0)
        #
        # affected_maps = dict()
        # for k, v in self.substMap.items():
        #     if item.item_id in v:
        #         v.remove(item.item_id)
        #         affected_maps[k] = v
        #
        # self._persistenceFacade.deleteDeviceItem(item, affected_maps)
        #
        # self.deviceMapModel.removeItem(item.item_id)
        #
        # self.deviceRemoved.emit(item.item_id)

    # def addVendorRecord(self, data):
    #     print("domain model add vendor record call", data)
    #     newId = self._persistenceFacade.addVendorRecord(data)
    #
    #     self.vendorList[newId] = data[0]
    #     self.vendorMapModel.addItem(newId, data[0])
    #
    #     print(self.vendorList)

    # def addDictRecord(self, dictName, data):
    #     print("domain model add dict record:", dictName, data)
    #     newId = self._persistenceFacade.addDictRecord(dictName, data)
    #
    #     if dictName == "vendor":
    #         self.vendorMapModel.addItem(newId, data)
    #     elif dictName == "devtype":
    #         self.devtypeMapModel.addItem(newId, data)

    # def editDictRecord(self, dictName, data):
    #     print("domain model edit dict record:", dictName, data)
    #     self._persistenceFacade.editDictRecord(dictName, data)
    #
    #     if dictName == "vendor":
    #         self.vendorMapModel.updateItem(data[0], data[1])
    #     elif dictName == "devtype":
    #         self.devtypeMapModel.updateItem(data[0], data[1])

    # def deleteDictRecord(self, dictName, data):
    #     print("domain model delete dict record:", dictName, data)
    #     if not self._persistenceFacade.checkDictRef(dictName, data):
    #
    #         self._persistenceFacade.deleteDictRecord(dictName, data)
    #
    #         if dictName == "vendor":
    #             self.vendorMapModel.removeItem(data)
    #         elif dictName == "devtype":
    #             self.vendorMapModel.removeItem(data)
    #         return True
    #     return False
