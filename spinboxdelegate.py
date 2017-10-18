import const
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyledItemDelegate, QSpinBox
from mapmodel import MapModel


class SpinBoxDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(SpinBoxDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() != 1:
            return super().createEditor(parent, option, index)
        spin = QSpinBox(parent=parent)
        spin.setSuffix(" шт.")
        spin.setMaximum(999999999)
        return spin

    def setEditorData(self, editor, index):
        if isinstance(editor, QSpinBox):
            editor.setValue(index.data(Qt.EditRole))
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(editor, QSpinBox):
            model.setData(index, editor.value(), Qt.EditRole)
        else:
            super().setModelData(editor, model, index)
