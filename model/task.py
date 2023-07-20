from typing import List, Union


class Task:
    start_time: str
    end_time: str
    name: str
    description: str
    done: bool
    hours: int

    def __init__(self, name: str, description: str, done: bool, start_time="", end_time="", hours=0, parent=None):
        self.tasks: List[Task] = []
        self.parent: Union[Task, None] = parent
        self.start_time = start_time
        self.end_time = end_time
        self.name = name
        self.description = description
        self.done = done
        self.hours = hours

    def get_start_time(self) -> str:
        result = self.start_time
        for task in self.tasks:
            task_time = task.get_start_time()
            if task_time != "":
                if result == "":
                    result = task_time
                result = min(result, task_time)
        return result

    def get_end_time(self) -> str:
        task_list = list(self.tasks)
        task_list.append(self)
        return max(map(Task.get_end_time, task_list))
