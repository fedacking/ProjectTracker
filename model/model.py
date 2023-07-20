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

    def add_task(self, task: Task):
        self._add_task_date(task)

        if task.parent is not None:
            task.parent.tasks.append(task)
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
