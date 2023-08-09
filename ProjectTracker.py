import sys
import os

from PyQt5 import QtWidgets

from model.model import model
from ui.main_window import MainWindow

if os.path.exists("data/.default.pkl"):
    with open("data/.default.pkl", "r+b") as file:
        model.import_model(file)
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()
with open("data/.default.pkl", "w+b") as file:
    model.export_model(file)
