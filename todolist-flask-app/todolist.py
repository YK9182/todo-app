# todolist.py
import json
from task import Task

class ToDoList:
    def __init__(self, filename='tasks.json'):
        self.tasks = []
        self.filename = filename
        self.load_from_file()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_to_file()

    def toggle_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].toggle()
            self.save_to_file()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_to_file()

    def get_task(self, index):
        return self.tasks[index] if 0 <= index < len(self.tasks) else None

    def sort_by_due_date(self):
        self.tasks.sort(key=lambda t: t.get_due_datetime() or float('inf'))
        self.save_to_file()

    def save_to_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([task.__dict__ for task in self.tasks], f, ensure_ascii=False, indent=2)

    def load_from_file(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.tasks = [Task(**item) for item in data]
        except FileNotFoundError:
            self.tasks = []
        except json.JSONDecodeError:
            self.tasks = []
