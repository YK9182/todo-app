# task.py
from datetime import datetime

class Task:
    def __init__(self, title, description='', due_date='', completed=False, tag='', priority='medium', created_at=None, completed_at=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed
        self.tag = tag
        self.priority = priority
        
        # created_atが提供されていない場合は現在時刻を設定
        if created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.created_at = created_at
            
        self.completed_at = completed_at
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("title", ""),
            data.get("description", ""),
            data.get("due_date", ""),
            data.get("completed", False),
            data.get("tag", ""),
            data.get("priority", "medium"),
            data.get("created_at"),
            data.get("completed_at")
        )

    def toggle(self):
        self.completed = not self.completed
        self.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if self.completed else None

    def is_overdue(self):
        if not self.due_date:
            return False
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
            return not self.completed and due < date.today()
        except:
            return False

    def get_due_datetime(self):
        if not self.due_date:
            return None
        try:
            return datetime.strptime(self.due_date, "%Y-%m-%d")
        except:
            return None

    def days_until_due(self):
        dt = self.get_due_datetime()
        if dt:
            return (dt.date() - datetime.now().date()).days
        return None

    def get_priority_color(self):
        return {
            'high': 'danger',
            'medium': 'warning',
            'low': 'secondary'
        }.get(self.priority, 'secondary')

    def get_priority_text(self):
        return {
            'high': '高',
            'medium': '中',
            'low': '低'
        }.get(self.priority, '中')

    def get_tag_color(self):
        return {
            '仕事': 'primary',
            '勉強': 'success',
            '買い物': 'warning'
        }.get(self.tag, 'secondary')

    def get_formatted_created_at(self):
        """作成日時を読みやすい形式で返す"""
        try:
            dt = datetime.strptime(self.created_at, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%Y年%m月%d日 %H:%M")
        except:
            return self.created_at

    def get_formatted_completed_at(self):
        """完了日時を読みやすい形式で返す"""
        if not self.completed_at:
            return None
        try:
            dt = datetime.strptime(self.completed_at, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%Y年%m月%d日 %H:%M")
        except:
            return self.completed_at