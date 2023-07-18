from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from model.model import model


def import_data():
    filename = QFileDialog.getOpenFileName(None, 'Open file', 'data', "Pickle Files (*.pickle *.pkl)")[0]
    if filename != "":
        with open(filename, "rb+") as file:
            model.import_model(file)


def export_data():
    filename = QFileDialog.getOpenFileName(None, 'Open file', 'data', "Pickle Files (*.pickle *.pkl)")[0]
    if filename != "":
        with open(filename, "wb+") as file:
            model.export_model(file)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/main_window.ui', self)
        self.action_import.triggered.connect(import_data)
        self.action_export.triggered.connect(export_data)
        self.show()
