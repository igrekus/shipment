import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
from reportlab.lib.testutils import setOutDir
setOutDir(__name__)


def main():
    # import csv
    # l = list()
    # with open("ref/items.csv") as f:
    #     d = csv.reader(f, delimiter=";")
    #     for a in d:
    #         detail = a[1] + ",'" + a[4] + "'," + a[5] + ")"
    #         print(detail)
    #         # if not a[31]:
    #         #     a[31] = '0'
    #         # string = "('" + a[0] + "'," + \
    #         #          a[1] + ",'" + \
    #         #          a[2] + "','" + \
    #         #          a[4].strip() + "','" + \
    #         #          a[5] + "','" + \
    #         #          a[6] + "','" + \
    #         #          a[7] + "','" + \
    #         #          a[8] + "','" + \
    #         #          a[9] + "','" + \
    #         #          a[10].strip() + "','" + \
    #         #          a[11] + "','" + \
    #         #          a[12] + "'," + \
    #         #          a[13].replace(" ", "").replace(",", "") + ",'" + \
    #         #          a[14].strip() + "','" + \
    #         #          a[15] + "','" + \
    #         #          a[16] + "','" + \
    #         #          a[17] + "','" + \
    #         #          a[18] + "','" + \
    #         #          a[19] + "','" + \
    #         #          a[20] + "','" + \
    #         #          a[21] + "','" + \
    #         #          a[24] + "','" + \
    #         #          a[25].strip() + "','" + \
    #         #          a[26] + "','" + \
    #         #          a[27].strip() + "','" + \
    #         #          a[28] + "','" + \
    #         #          a[29] + "','" + \
    #         #          a[30] + "'," + \
    #         #          a[31].replace("*", "1") + ",'" + \
    #         #          a[32] + "')"
    #         # detail = a[0] + ';' + a[3]
    #         l.append(detail)
    #
    # with open("ref/detail.sql", "w") as f:
    #     for s in l:
    #         f.write(s+",\n")

    app = QApplication(sys.argv)
    # app.setStyle("macintosh")
    w = MainWindow()
    w.initApp()
    # w.showMaximized()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


