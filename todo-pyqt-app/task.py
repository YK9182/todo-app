class Task:
    def __init__(self, title, description, due_date=None, completed=False, tag=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed
        self.tag = tag

    def mark_complete(self):
        self.completed = True

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "completed": self.completed,
            "tag": self.tag
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data.get("description"),
            data.get("due_date"),
            data.get("completed", False),
            data.get("tag")
        )

    def __str__(self):
        return f"[{'✓' if self.completed else ' '}] {self.title} - {self.description} - {self.due_date}- {self.tag or '未分類'}"