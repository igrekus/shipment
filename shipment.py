import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
from reportlab.lib.testutils import setOutDir
setOutDir(__name__)


def main():
    # import csv
    # l = list()
    # with open("ref/tnew.csv") as f:
    #     d = csv.reader(f, delimiter=";")
    #     for a in d:
            # print(print(len(a), a))
            # string = "('" + a[0] + "'," + \
            #          a[1] + ",'" + \
            #          a[2] + "','" + \
            #          a[4].strip() + "','" + \
            #          a[5] + "','" + \
            #          a[6] + "','" + \
            #          a[7] + "','" + \
            #          a[8] + "','" + \
            #          a[9] + "','" + \
            #          a[10].strip() + "','" + \
            #          a[11] + "','" + \
            #          a[12] + "'," + \
            #          a[13].replace(" ", "").replace(",", "") + ",'" + \
            #          a[14].strip() + "','" + \
            #          a[15] + "','" + \
            #          a[16] + "','" + \
            #          a[17] + "','" + \
            #          a[18] + "','" + \
            #          a[19] + "','" + \
            #          a[20] + "','" + \
            #          a[21] + "','" + \
            #          a[24] + "','" + \
            #          a[25].strip() + "','" + \
            #          a[26] + "','" + \
            #          a[27].strip() + "','" + \
            #          a[28] + "','" + \
            #          a[29] + "','" + \
            #          a[30] + "'," + \
            #          a[31].replace("*", "1") + ",'" + \
            #          a[32] + "')"

    #         string = "UPDATE contract SET contract_requestDate = STR_TO_DATE('" + a[6].strip() + "', '%d.%m.%Y')," + \
    #                  "contract_dogozDate = STR_TO_DATE('" + a[8].strip() + "', '%d.%m.%Y')," + \
    #                  "contract_contractDate = STR_TO_DATE('" + a[12].strip() + "', '%d.%m.%Y')," + \
    #                  "contract_specReturnDate = STR_TO_DATE('" + a[13].strip() + "', '%d.%m.%Y')," + \
    #                  "contract_billDate = STR_TO_DATE('" + a[16].strip() + "', '%d.%m.%Y')," + \
    #                  "contract_milDate = STR_TO_DATE('" + a[17].strip() + "', '%d.%m.%Y')," + \
    #                  "contract_addLetterDate = STR_TO_DATE('" + a[18].strip() + "', '%d.%m.%Y')," + \
    #                  "contract_responseDate = STR_TO_DATE('" + a[19].strip() + "', '%d.%m.%Y')," + \
    #                  "contract_paymentDate = STR_TO_DATE('" + a[21].strip() + "', '%d.%m.%Y')," + \
    #                  "contract_matPurchaseDate = STR_TO_DATE('" + a[22].strip() + "', '%d.%m.%Y')," + \
    #                  "contract_invoiceDate = STR_TO_DATE('" + a[28].strip() + "', '%d.%m.%Y')," + \
    #                  "contract_packingListDate = STR_TO_DATE('" + a[30].strip() + "', '%d.%m.%Y')," + \
    #                  "contract_shipDate = STR_TO_DATE('" + a[32].strip() + "', '%d.%m.%Y') WHERE contract_index = '" + \
    #                  "" + a[0].strip().strip(",") + "'"
    #         print(string)
    #         l.append(string)
    #
    # with open("ref/dates.sql", "w") as f:
    #     for s in l:
    #         f.write(s+";\n")

    # TODO: add new field
    app = QApplication(sys.argv)
    # app.setStyle("macintosh")
    w = MainWindow()
    w.initApp()
    # w.showMaximized()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


