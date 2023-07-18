import sys

from PyQt5 import QtWidgets

from ui.main_window import MainWindow

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()
