import const
from contractitem import ContractItem
from mapmodel import MapModel
from PyQt5.QtCore import QObject, pyqtSignal


class DomainModel(QObject):

    contractAdded = pyqtSignal(int)
    contractUpdated = pyqtSignal(int)
    contractRemoved = pyqtSignal(int)

    def __init__(self, parent=None, persistenceFacade=None):
        super(DomainModel, self).__init__(parent)

        self._persistenceFacade = persistenceFacade

        self.contractList = dict()
        self.contractDetailList = dict()
        self.dicts = dict()

        self.clientMapModel: MapModel = None
        self.productMapModel: MapModel = None

        self.dictList = [const.DICT_CLIENT, const.DICT_PRODUCT]

    def buildMapModel(self, name: str):
        self.dicts[name] = MapModel(self, self._persistenceFacade.getDict(name))
        self.dicts[name].addItemAtPosition(0, 0, "Все")

    def initModel(self):
        print("init domain model")
        self.contractList = self._persistenceFacade.getContractList()
        self.contractDetailList = self._persistenceFacade.getContractDetailList()

        # FIXME: make uniform dict
        for name in self.dictList:
            self.buildMapModel(name)
        self.dicts[const.DICT_PRICE] = self._persistenceFacade.getDict(const.DICT_PRICE)

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
        print("updates", updates)

        self.contractList[item.item_id] = item
        self.contractDetailList[item.item_id] = products

        self._persistenceFacade.updateContractItem(item, updates)

        self.contractUpdated.emit(item.item_id)

    def deleteContractItem(self, item: ContractItem):
        print("domain model delete contract item call:", item)
        print("deleting bound products")

        self.contractList.pop(item.item_id, 0)
        self.contractDetailList.pop(item.item_id, 0)

        self._persistenceFacade.deleteContractItem(item)

        self.contractRemoved.emit(item.item_id)

    def addDictRecord(self, name, data):
        print("domain model add dict record:", name, data)
        newId = self._persistenceFacade.addDictRecord(name, data)
        self.dicts[name].addItem(newId, data)

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
