from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QStyledItemDelegate, QDateEdit


class DateEditDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(DateEditDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() != 3:
            return super().createEditor(parent, option, index)

        de = QDateEdit(parent=parent)
        de.setCalendarPopup(True)
        de.setDate(QDate().currentDate())
        return de

    def setEditorData(self, editor, index):
        if isinstance(editor, QDateEdit):
            editor.setDate(index.data(Qt.EditRole))
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(editor, QDateEdit):
            model.setData(index, editor.date(), Qt.EditRole)
        else:
            super().setModelData(editor, model, index)
