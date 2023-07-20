from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from model.model import model
from model.task import Task
from .task_view import TreeModel


class TaskDialog(QDialog):
    parent: Task

    def __init__(self, item_model, parent: Task = None):
        super(QDialog, self).__init__()
        uic.loadUi('ui/task_dialog.ui', self)
        self.button_box.accepted.connect(self.add_task)
        self.parent = parent
        self.item_model: TreeModel = item_model

    def add_task(self):
        start_time = self.start_date_edit.dateTime().toTimeSpec(Qt.UTC).toString(Qt.ISODate)
        end_time = self.end_date_edit.dateTime().toTimeSpec(Qt.UTC).toString(Qt.ISODate)
        if start_time == '2000-01-01T03:00:00Z':
            start_time = ""
        if end_time == '2000-01-01T03:00:00Z':
            end_time = ""
        new_task = Task(
            self.name_textbox.text(),
            self.description_textbox.toPlainText(),
            bool(self.done_checkbox.checkState()),
            start_time,
            end_time,
            self.hours_spinbox.value(),
            self.parent
        )
        model.add_task(new_task)
        self.item_model.modelReset.emit()
