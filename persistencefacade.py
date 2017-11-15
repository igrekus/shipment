from collections import defaultdict

from mapmodel import MapModel
from PyQt5.QtCore import QObject

from contractitem import ContractItem


class PersistenceFacade(QObject):

    def __init__(self, parent=None, persistenceEngine=None):
        super(PersistenceFacade, self).__init__(parent)

        self._engine = persistenceEngine
        self.engineType = self._engine._engineType

    def initFacade(self):
        print("init persistence facade:", self._engine._engineType)

    def getContractList(self):
        return {r[0]: ContractItem.fromSqlTuple(r) for r in self._engine.fetchMainData()}

    def getContractDetailList(self):
        d = defaultdict(list)
        for r in self._engine.fetchContractDetailList():
            d[r[0]].append([r[1], r[2], r[3]])
        return d

    def getDict(self, name):
        return {r[0]: r[1] for r in self._engine.fetchDict(name)}

    # def getSubstMap(self):
    #     substmap = defaultdict(set)
    #     for r in self._engine.fetchSubstMap():
    #         for s in r[1].split(","):
    #             if s:
    #                 substmap[r[0]].add(int(s))
    #     return substmap

    # def getVendorDict(self):
    #     return {v[0]: [v[1], v[2]] for v in self._engine.fetchVendorList()}
    #
    # def getDevtypeDict(self):
    #     return {v[0]: v[1] for v in self._engine.fetchDevtypeList()}

    def insertContractItem(self, item: ContractItem, products: list):
        print("persistence facade insert device item call:", item, products)

        newContractId = self._engine.insertMainDataRecord(item.toTuple())
        newDetailIdList = self._engine.insertContractDetail(products)

        item.item_id = newContractId

        newDetailList = [[i, d[1], d[2]] for i, d in zip(newDetailIdList, products)]

        return item, newDetailList

    def updateContractItem(self, item: ContractItem, updates: list):
        print("persistence facade update device item call:", item)
        print("products", updates)
        # self._engine.updateDeviceRecord(item.toTuple())
        # self.updateAffectedMaps(affected_maps)

    # def updateAffectedMaps(self, maps: dict):
    #     print("persistence facade update affected maps call:", maps)
    #     tmplist = list()
    #     for k, v in maps.items():
    #         string = str()
    #         for i in v:
    #             string += str(i) + ","
    #         tmplist.append((k, string.strip(","), ))
    #
    #     self._engine.updateDeviceMappings(tmplist)
    #
    # def deleteDeviceItem(self, item: DeviceItem, affected_maps: dict):
    #     print("persistence facade delete item call:", item)
    #     self._engine.deleteDeviceRecord(item.toTuple())
    #     self.updateAffectedMaps(affected_maps)
    #
    # def addVendorRecord(self, data: list):
    #     print("persistence facade add vendor record:", data)
    #     return self._engine.insertVendorRecord(data)
    #
    # def addDictRecord(self, dictName, data):
    #     print("persistence facade add dict record:", dictName, data)
    #     return self._engine.insertDictRecord(dictName, (data, ))
    #
    # def editDictRecord(self, dictName, data):
    #     print("persistence facade add dict record:", dictName, data)
    #     self._engine.updateDictRecord(dictName, (data[1], data[0]))
    #
    # def deleteDictRecord(self, dictName, data):
    #     print("persistence facade add dict record:", dictName, data)
    #     self._engine.deleteDictRecord(dictName, (data, ))
    #
    # def checkDictRef(self, dictName, data):
    #     print("persistence facade check dict ref:", dictName, data)
    #     return self._engine.checkDictRef(dictName, data)
