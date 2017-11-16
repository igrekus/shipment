from PyQt5.QtCore import Qt

ORIGIN_IMPORT = 1
ORIGIN_HOMEBREW = 2

DICT_CLIENT = "client"
DICT_PRODUCT = "product"

COLOR_PAYMENT_FINISHED = 0xff92D050
COLOR_PAYMENT_PENDING = 0xffFF6767

COLOR_PRIORITY_LOW = 0xffAABF00
COLOR_PRIORITY_MEDIUM = 0xffFFFF00
COLOR_PRIORITY_HIGH = 0xffFFFF00

COLOR_ARRIVAL_PENDING = 0xffFF6767
COLOR_ARRIVAL_PARTIAL = 0xffFF9462
COLOR_ARRIVAL_RECLAIM = 0xffFF6767

RoleNodeId = Qt.UserRole + 1
RoleClient = RoleNodeId + 1
RoleProduct = RoleClient + 1
