from PyQt5 import uic
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import QDialog

from model.model import model
from model.task import Task
from .task_view import TreeModel


class TaskDialog(QDialog):
    parent: Task

    def __init__(self, item_model, current_task: Task = None, parent: Task = None):
        super(QDialog, self).__init__()
        uic.loadUi('ui/task_dialog.ui', self)
        self.button_box.accepted.connect(self.add_task)
        self.current_task = current_task
        self.parent = parent
        if current_task is not None:
            self.parent = current_task.parent
            self.name_textbox.setText(current_task.name)
            self.description_textbox.insertPlainText(current_task.description)
            self.start_date_edit.setDateTime(
                QDateTime.fromString(current_task.start_time, Qt.ISODate).toTimeSpec(Qt.TimeZone))
            self.end_date_edit.setDateTime(
                QDateTime.fromString(current_task.end_time, Qt.ISODate).toTimeSpec(Qt.TimeZone))
            self.hours_spinbox.setValue(current_task.hours)
            self.done_checkbox.setChecked(current_task.done)
        if self.parent is not None:
            self.parent_label.setText('Parent Task: ' + parent.name)
        self.item_model: TreeModel = item_model

    def add_task(self):
        start_time = self.start_date_edit.dateTime().toString(Qt.ISODate)
        end_time = self.end_date_edit.dateTime().toString(Qt.ISODate)
        if start_time == '2000-01-01T00:00:00':
            start_time = ""
        else:
            start_time = self.start_date_edit.dateTime().toTimeSpec(Qt.UTC).toString(Qt.ISODate)
        if end_time == '2000-01-01T00:00:00':
            end_time = ""
        else:
            end_time = self.end_date_edit.dateTime().toTimeSpec(Qt.UTC).toString(Qt.ISODate)

        if self.current_task is not None:
            self.current_task.name = self.name_textbox.text()
            self.current_task.description = self.description_textbox.toPlainText()
            self.current_task.done = bool(self.done_checkbox.checkState())
            self.current_task.start_time = start_time
            self.current_task.end_time = end_time
            self.current_task.hours = self.hours_spinbox.value()
            self.current_task.parent = self.parent
        else:
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
