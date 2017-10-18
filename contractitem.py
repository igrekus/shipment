import const


class ContractItem:
    # TODO: make DB-aware orm?
    # TODO: make properties
    def __init__(self, id_=None, index=None, clientRef=None, projCode=None, requestN=None, requestDate=None,
                 dogozName=None, dogozDate=None, deviceRequestN=None, deviceRequestCode=None, contractN=None,
                 contractDate=None, specReturnDate=None, sum=None, billNumber=None, billDate=None, milDate=None,
                 addLetterDate=None, responseDate=None, paymentOrderN=None, paymentDate=None,
                 matPurchaseDate=None, planShipmentDate=None,
                 shipmentPeriod=None, invoiceN=None, invoiceDate=None, packingListN=None, packingListDate=None,
                 shipNote=None, shipDate=None, completed=None, contacts=None, manufPlanDate=None):
        self.item_id = id_
        self.item_index = index
        self.item_clientRef = clientRef
        self.item_projCode = projCode
        self.item_requestN = requestN
        self.item_requestDate = requestDate
        self.item_dogozName = dogozName
        self.item_dogozDate = dogozDate
        self.item_deviceRequestN = deviceRequestN
        self.item_deviceRequestCode = deviceRequestCode
        self.item_contractN = contractN
        self.item_contractDate = contractDate
        self.item_specReturnDate = specReturnDate
        self.item_sum = sum
        self.item_billNumber = billNumber
        self.item_billDate = billDate
        self.item_milDate = milDate
        self.item_addLetterDate = addLetterDate
        self.item_responseDate = responseDate
        self.item_paymentOrderN = paymentOrderN
        self.item_paymentDate = paymentDate
        self.item_matPurchaseDate = matPurchaseDate
        self.item_planShipmentDate = planShipmentDate
        self.item_shipmentPeriod = shipmentPeriod
        self.item_invoiceN = invoiceN
        self.item_invoiceDate = invoiceDate
        self.item_packingListN = packingListN
        self.item_packingListDate = packingListDate
        self.item_shipNote = shipNote
        self.item_shipDate = shipDate
        self.item_completed = completed
        self.item_contacts = contacts
        self.item_manufPlanDate = manufPlanDate

    def __str__(self):
        return "ContractItem(" + "id:" + str(self.item_id) + " " \
               + "idx:" + str(self.item_index) + " " \
               + "cref:" + str(self.item_clientRef) + " " \
               + "proj:" + str(self.item_projCode) + " " \
               + "reqn:" + str(self.item_requestN) + " " \
               + "reqd:" + str(self.item_requestDate) + " " \
               + "dogn:" + str(self.item_dogozName) + " " \
               + "dogd:" + str(self.item_dogozDate) + " " \
               + "devreqn:" + str(self.item_deviceRequestN) + " " \
               + "devreqc:" + str(self.item_deviceRequestCode) + " " \
               + "conn:" + str(self.item_contractN) + " " \
               + "cond:" + str(self.item_contractDate) + " " \
               + "specretd:" + str(self.item_specReturnDate) + " " \
               + "sum:" + str(self.item_sum) + " " \
               + "billn:" + str(self.item_billNumber) + " " \
               + "billd:" + str(self.item_billDate) + " " \
               + "mild:" + str(self.item_milDate) + " " \
               + "addld:" + str(self.item_addLetterDate) + " " \
               + "respd:" + str(self.item_responseDate) + " " \
               + "payn:" + str(self.item_paymentOrderN) + " " \
               + "payd:" + str(self.item_paymentDate) + " "\
               + "matd:" + str(self.item_matPurchaseDate) + " " \
               + "pland:" + str(self.item_planShipmentDate) + " " \
               + "period:" + str(self.item_shipmentPeriod) + " " \
               + "invn:" + str(self.item_invoiceN) + " " \
               + "invd:" + str(self.item_invoiceDate) + " " \
               + "packn:" + str(self.item_packingListN) + " " \
               + "packd:" + str(self.item_packingListDate) + " " \
               + "shipn:" + str(self.item_shipNote) + " " \
               + "shipd:" + str(self.item_shipDate) + " " \
               + "compl:" + str(self.item_completed) + " " \
               + "contact:" + str(self.item_contacts) + " " \
               + "manuf:" + str(self.item_manufPlanDate) + ")"

    @classmethod
    def fromSqlTuple(cls, sql_tuple: tuple):
        return cls(id_=sql_tuple[0],
                   index=sql_tuple[1],
                   clientRef=sql_tuple[2],
                   projCode=sql_tuple[3],
                   requestN=sql_tuple[4],
                   requestDate=sql_tuple[5],
                   dogozName=sql_tuple[6],
                   dogozDate=sql_tuple[7],
                   deviceRequestN=sql_tuple[8],
                   deviceRequestCode=sql_tuple[9],
                   contractN=sql_tuple[10],
                   contractDate=sql_tuple[11],
                   specReturnDate=sql_tuple[12],
                   sum=sql_tuple[13],
                   billNumber=sql_tuple[14],
                   billDate=sql_tuple[15],
                   milDate=sql_tuple[16],
                   addLetterDate=sql_tuple[17],
                   responseDate=sql_tuple[18],
                   paymentOrderN=sql_tuple[19],
                   paymentDate=sql_tuple[20],
                   matPurchaseDate=sql_tuple[21],
                   planShipmentDate=sql_tuple[22],
                   shipmentPeriod=sql_tuple[23],
                   invoiceN=sql_tuple[24],
                   invoiceDate=sql_tuple[25],
                   packingListN=sql_tuple[26],
                   packingListDate=sql_tuple[27],
                   shipNote=sql_tuple[28],
                   shipDate=sql_tuple[29],
                   completed=sql_tuple[30],
                   contacts=sql_tuple[31],
                   manufPlanDate=sql_tuple[32])

    def toTuple(self):
        return tuple([self.item_index,
                      self.item_clientRef,
                      self.item_projCode,
                      self.item_requestN,
                      self.item_requestDate,
                      self.item_dogozName,
                      self.item_dogozDate,
                      self.item_deviceRequestN,
                      self.item_deviceRequestCode,
                      self.item_contractN,
                      self.item_contractDate,
                      self.item_specReturnDate,
                      self.item_sum,
                      self.item_billNumber,
                      self.item_billDate,
                      self.item_milDate,
                      self.item_addLetterDate,
                      self.item_responseDate,
                      self.item_paymentOrderN,
                      self.item_paymentDate,
                      self.item_matPurchaseDate,
                      self.item_planShipmentDate,
                      self.item_shipmentPeriod,
                      self.item_invoiceN,
                      self.item_invoiceDate,
                      self.item_packingListN,
                      self.item_packingListDate,
                      self.item_shipNote,
                      self.item_shipDate,
                      self.item_completed,
                      self.item_contacts,
                      self.item_manufPlanDate,
                      self.item_id])

    @classmethod
    def itemListRequestString(self):
        return str("CALL getContractList()")
