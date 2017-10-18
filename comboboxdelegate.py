import const
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox
from mapmodel import MapModel


class ComboBoxDelegate(QStyledItemDelegate):

    def __init__(self, parent=None, mapModel: MapModel=None):
        super(ComboBoxDelegate, self).__init__(parent)

        self.comboMapModel = mapModel

    def createEditor(self, parent, option, index):
        if index.column() != 0:
            return super().createEditor(parent, option, index)
        combo = QComboBox(parent=parent)
        combo.setModel(self.comboMapModel)
        combo.setEditable(False)
        return combo

    def setEditorData(self, editor, index):
        if isinstance(editor, QComboBox):
            editor.setCurrentText(index.data(Qt.DisplayRole))
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(editor, QComboBox):
            model.setData(index, editor.currentData(const.RoleNodeId), Qt.EditRole)
        else:
            super().setModelData(editor, model, index)
