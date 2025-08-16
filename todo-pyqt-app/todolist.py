import json
from task import Task
from datetime import datetime

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        self.save_to_file()

    def show_tasks(self):
        if not self.tasks:
            print("タスクがありません。")
        for i, task in enumerate(self.tasks, start=1):
            print(f"{i}. {task}")

    def save_to_file(self, filename="tasks.json"):
        with open(filename, "w", encoding="utf-8") as f:
            data = [task.to_dict() for task in self.tasks]
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_file(self, filename="tasks.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]
        except FileNotFoundError:
            print("保存ファイルが見つかりませんでした。新しく始めます。")
        except json.JSONDecodeError:
            print("ファイルの読み込みに失敗しました。ファイルが壊れている可能性があります。")
    
    def toggle_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = not self.tasks[index].completed
            self.save_to_file()
            print("完了状態を切り替えました。")
        else:
            print("無効な番号です。")
    
    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            self.save_to_file()
            print(f"「{removed.title}」を削除しました。")
        else:
            print("無効な番号です。")

    def sort_by_due_date(self):
        def parse_date(task):
            try:
                return datetime.strptime(task.due_date, "%Y/%m/%d")
            except (TypeError, ValueError):
                return datetime.max  # 日付がない or 不正なら一番最後に

        self.tasks.sort(key=parse_date)
        print("締切日順に並び替えました。")

    def show_incomplete_tasks(self):
        has_tasks = False
        for i, task in enumerate(self.tasks, start=1):
            if not task.completed:
                print(f"{i}. {task}")
                has_tasks = True
        if not has_tasks:
            print("未完了のタスクはありません。")
    
    def show_tasks_by_tag(self, tag):
        filtered = [task for task in self.tasks if task.tag == tag]
        if not filtered:
            print(f"「{tag}」カテゴリのタスクはありません。")
            return
        for i, task in enumerate(filtered, 1):
            print(f"{i}. {task}")

    def search_tasks_by_keyword(self, keyword):
        results = [task for task in self.tasks if keyword.lower() in task.title.lower()]
        if not results:
            print(f"「{keyword}」を含むタスクは見つかりませんでした。")
        else:
            for i, task in enumerate(results, 1):
                print(f"{i}. {task}")
