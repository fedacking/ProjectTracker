import pickle
from typing import BinaryIO, List, Dict

from .task import Task


class Model:
    tasks: List[Task]
    dates: Dict[str, List[str]]

    def import_model(self, file: BinaryIO):
        self.tasks, self.dates = pickle.load(file)

    def export_model(self, file: BinaryIO):
        pickle.dump((self.tasks, self.dates), file)


model = Model()
