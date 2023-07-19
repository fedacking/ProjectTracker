from PyQt5.QtCore import QAbstractItemModel, QModelIndex

from model.model import model


class TreeModel (QAbstractItemModel):

    def __init__(self):
        super(QAbstractItemModel, self).__init__()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 5

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if parent is not None and parent.row() > -1:
            return parent.row()
        return len(model.tasks)

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        return self.createIndex(row, column, model.tasks[row].name)
