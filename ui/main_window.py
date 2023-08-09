from PyQt5 import uic
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QTreeView, QMenu, QAction

from model.model import model
from .task_view import TreeModel
from .task_dialog import TaskDialog


class MainWindow(QMainWindow):
    dialog: TaskDialog
    task_view: QTreeView

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/main_window.ui', self)
        self.action_import.triggered.connect(import_data)
        self.action_export.triggered.connect(export_data)
        self.task_add_button.clicked.connect(self.open_task_dialog)
        self.task_model = TreeModel(self.task_view)
        self.task_view.setModel(self.task_model)
        self.task_view.expandAll()

        # Context Menu stuff
        self.task_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.task_view.customContextMenuRequested.connect(self.context_menu)
        self.context_menu_widget = QMenu(self.task_view)
        # add Action
        add_action = QAction("Add", self)
        add_action.triggered.connect(lambda: self.open_task_dialog(True))
        self.context_menu_widget.addAction(add_action)
        # Edit Action
        edit_action = QAction("Edit", self)
        edit_action.triggered.connect(self.edit_task_dialog)
        self.context_menu_widget.addAction(edit_action)
        # Delete Action
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self.task_model.delete_task)
        self.context_menu_widget.addAction(delete_action)

        self.show()

    def open_task_dialog(self, use_parent=False):
        if use_parent:
            self.dialog = TaskDialog(self.task_model, parent=self.task_model.context_menu_index.internalPointer())
        else:
            self.dialog = TaskDialog(self.task_model)
        self.dialog.show()

    def edit_task_dialog(self):
        self.dialog = TaskDialog(self.task_model, self.task_model.context_menu_index.internalPointer())
        self.dialog.show()

    def context_menu(self, point: QPoint):
        self.task_model.context_menu_index = self.task_view.indexAt(point)
        self.context_menu_widget.exec(self.task_view.viewport().mapToGlobal(point))


def import_data():
    filename = QFileDialog.getOpenFileName(None, 'Open file', 'data', "Pickle Files (*.pkl *.pickle)")[0]
    if filename != "":
        with open(filename, "rb+") as file:
            model.import_model(file)


def export_data():
    filename = QFileDialog.getSaveFileName(None, 'Save file', 'data', "Pickle Files (*.pkl *.pickle)")[0]
    if filename != "":
        with open(filename, "wb+") as file:
            model.export_model(file)
