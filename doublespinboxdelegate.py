from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyledItemDelegate, QDoubleSpinBox


class DoubleSpinBoxDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(DoubleSpinBoxDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() != 1:
            return super().createEditor(parent, option, index)
        spin = QDoubleSpinBox(parent=parent)
        spin.setSuffix(" руб.")
        spin.setMaximum(999999999)
        spin.setDecimals(2)
        return spin

    def setEditorData(self, editor, index):
        if isinstance(editor, QDoubleSpinBox):
            editor.setValue(index.data(Qt.EditRole))
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(editor, QDoubleSpinBox):
            model.setData(index, editor.value(), Qt.EditRole)
        else:
            super().setModelData(editor, model, index)
