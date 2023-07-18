from typing import List


class Task:
    start_time: str
    end_time: str

    def __init__(self):
        self.tasks: List[Task] = []
        self.start_time = ""
        self.end_time = ""

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
