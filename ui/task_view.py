from typing import Any

from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QVariant, Qt, QPoint
from PyQt5.QtWidgets import QMenu, QTreeView, QAction

from model.model import model
from model.task import Task


class TreeModel(QAbstractItemModel):
    header = ("Name", "Description", "Done", "Start Date", "End Date")
    context_menu_index: QModelIndex

    def __init__(self, view: QTreeView):
        super(QAbstractItemModel, self).__init__()
        self.view = view
        self.modelReset.connect(self.onModelReset)

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            child_item = model.tasks[row]
        else:
            child_item = parent.internalPointer().tasks[row]

        return self.createIndex(row, column, child_item)

    def parent(self, child: QModelIndex) -> QModelIndex:
        if not child.isValid():
            return QModelIndex()

        parent: Task = child.internalPointer().parent

        if parent is None:
            return QModelIndex()
        if parent.parent is None:
            return self.createIndex(model.tasks.index(parent), 0, parent)

        return self.createIndex(parent.parent.tasks.index(parent), 0, parent)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 5

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            return len(model.tasks)

        return len(parent.internalPointer().tasks)

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()

        task: Task = index.internalPointer()

        if index.column() == 0:
            return task.name
        if index.column() == 1:
            return task.description
        if index.column() == 2:
            return "✔" if task.done else "❌"
        if index.column() == 3:
            return task.get_start_time()
        return task.get_end_time()

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled or QAbstractItemModel.flags(self, index)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if orientation != Qt.Horizontal or role != Qt.DisplayRole:
            return QVariant()

        return self.header[section]

    def edit_task(self):
        print(self.context_menu_index.internalPointer())

    def delete_task(self):
        task: Task = self.context_menu_index.internalPointer()
        if task.parent is not None:
            task.parent.tasks.remove(task)
        else:
            model.tasks.remove(task)
        self.modelReset.emit()

    def onModelReset(self) -> None:
        self.view.expandAll()
