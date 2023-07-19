from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from model.model import model
from .task_view import TreeModel


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/main_window.ui', self)
        self.action_import.triggered.connect(import_data)
        self.action_export.triggered.connect(export_data)
        self.task_view.setModel(TreeModel())
        self.show()


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
