from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from model.model import model
from .task_view import TreeModel
from .task_dialog import TaskDialog


class MainWindow(QMainWindow):
    dialog: TaskDialog

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/main_window.ui', self)
        self.action_import.triggered.connect(import_data)
        self.action_export.triggered.connect(export_data)
        self.task_add_button.clicked.connect(self.open_task_dialog)
        self.task_model = TreeModel()
        self.task_view.setModel(self.task_model)
        self.show()

    def open_task_dialog(self):
        self.dialog = TaskDialog(self.task_model)
        self.dialog.show()


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
