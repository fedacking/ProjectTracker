import pickle
from typing import BinaryIO, List, Dict

from .task import Task


class Model:
    tasks: List[Task]
    dates: Dict[str, List[Task]]

    def __init__(self):
        self.dates = {}
        self.tasks = []

    def import_model(self, file: BinaryIO):
        self.tasks, self.dates = pickle.load(file)
        self.refresh_dates()

    def export_model(self, file: BinaryIO):
        pickle.dump((self.tasks, self.dates), file)

    def add_task(self, task: Task, parent_task: Task = None):
        self._add_task_date(task)

        if parent_task is not None:
            parent_task.tasks.append(task)
        else:
            self.tasks.append(task)

    def _add_task_date(self, task: Task):
        if task.get_start_time() != "":
            if task.get_start_time()[:10] not in self.dates:
                self.dates[task.get_start_time()[:10]] = []
            self.dates[task.get_start_time()[:10]].append(task)

    def _refresh_dates(self, tasks: List[Task]):
        for task in tasks:
            self._add_task_date(task)
            self._refresh_dates(task.tasks)

    def refresh_dates(self):
        self.dates = {}
        self._refresh_dates(self.tasks)


model = Model()
new_task = Task("Crear Calendario", "Tener el calendario Creado", False, "2023‐07‐18T19:00:00Z")
model.add_task(new_task)
