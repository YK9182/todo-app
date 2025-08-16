import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLineEdit, QLabel,
    QMessageBox, QListWidgetItem, QFormLayout, QMenu, QInputDialog
)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from task import Task
from todolist import ToDoList

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToDoアプリ - PyQt版")
        self.resize(800, 500)
        self.todo_list = ToDoList()
        self.todo_list.load_from_file()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # ステータスラベル
        self.status_label = QLabel("現在の表示：すべてのタスク")
        layout.addWidget(self.status_label)

        # タスクリスト表示
        self.list_widget = QListWidget()
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.open_context_menu)
        layout.addWidget(self.list_widget)

        # 入力欄
        self.title_input = QLineEdit()
        self.desc_input = QLineEdit()
        self.due_input = QLineEdit()
        self.tag_input = QLineEdit()

        self.title_input.setPlaceholderText("タイトル")
        self.desc_input.setPlaceholderText("説明")
        self.due_input.setPlaceholderText("締切日（例: 2024/12/31）")
        self.tag_input.setPlaceholderText("タグ（例: 勉強）")

        form_layout = QFormLayout()
        form_layout.addRow("タイトル", self.title_input)
        form_layout.addRow("説明", self.desc_input)
        form_layout.addRow("締切日", self.due_input)
        form_layout.addRow("タグ", self.tag_input)
        layout.addLayout(form_layout)

        # ボタン
        button_layout = QHBoxLayout()

        add_btn = QPushButton("追加")
        add_btn.clicked.connect(self.add_task)
        button_layout.addWidget(add_btn)

        reset_btn = QPushButton("すべて表示に戻す")
        reset_btn.clicked.connect(self.reset_filter)
        button_layout.addWidget(reset_btn)

        filter_tag_btn = QPushButton("タグで絞り込み")
        filter_tag_btn.clicked.connect(self.filter_by_tag)
        button_layout.addWidget(filter_tag_btn)

        filter_incomplete_btn = QPushButton("未完了のみ表示")
        filter_incomplete_btn.clicked.connect(self.filter_incomplete)
        button_layout.addWidget(filter_incomplete_btn)

        search_btn = QPushButton("キーワード検索")
        search_btn.clicked.connect(self.search_tasks)
        button_layout.addWidget(search_btn)

        sort_btn = QPushButton("締切日順に並び替え")
        sort_btn.clicked.connect(self.sort_by_due_date)
        button_layout.addWidget(sort_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.update_list()

    def add_task(self):
        title = self.title_input.text().strip()
        desc = self.desc_input.text().strip()
        due = self.due_input.text().strip()
        tag = self.tag_input.text().strip()

        if not title:
            QMessageBox.warning(self, "エラー", "タイトルを入力してください")
            return

        task = Task(title, desc, due, False, tag)
        self.todo_list.add_task(task)
        self.clear_inputs()
        self.update_list()

    def clear_inputs(self):
        self.title_input.clear()
        self.desc_input.clear()
        self.due_input.clear()
        self.tag_input.clear()

    def update_list(self, tasks=None, message="現在の表示：すべてのタスク"):
        self.list_widget.clear()
        self.status_label.setText(message)
        tasks = tasks if tasks is not None else self.todo_list.tasks

        tag_colors = {
            "勉強": QColor("#ccf2ff"),
            "仕事": QColor("#ffffcc"),
            "買い物": QColor("#ffebcc")
        }

        for task in tasks:
            item = QListWidgetItem(str(task))
            if task.completed:
                item.setBackground(QColor("#d3d3d3"))
                font = item.font()
                font.setStrikeOut(True)
                item.setFont(font)
                item.setForeground(QColor("#888888"))
            else:
                item.setBackground(tag_colors.get(task.tag, QColor("white")))
            self.list_widget.addItem(item)

    def open_context_menu(self, position):
        index = self.list_widget.currentRow()
        if index < 0:
            return

        menu = QMenu()
        toggle_action = menu.addAction("完了を切り替え")
        delete_action = menu.addAction("削除")
        edit_action = menu.addAction("編集")

        action = menu.exec_(self.list_widget.viewport().mapToGlobal(position))

        if action == toggle_action:
            self.todo_list.toggle_task(index)
        elif action == delete_action:
            self.todo_list.delete_task(index)
        elif action == edit_action:
            self.edit_task(index)

        self.update_list()

    def edit_task(self, index):
        task = self.todo_list.tasks[index]
        new_title, ok1 = QInputDialog.getText(self, "編集 - タイトル", "タイトル:", text=task.title)
        if not ok1:
            return
        new_desc, ok2 = QInputDialog.getText(self, "編集 - 説明", "説明:", text=task.description or "")
        if not ok2:
            return
        new_due, ok3 = QInputDialog.getText(self, "編集 - 締切日", "締切日 (例: 2024/12/31):", text=task.due_date or "")
        if not ok3:
            return
        new_tag, ok4 = QInputDialog.getText(self, "編集 - タグ", "タグ:", text=task.tag or "")
        if not ok4:
            return

        task.title = new_title
        task.description = new_desc
        task.due_date = new_due
        task.tag = new_tag
        self.todo_list.save_to_file()
        self.update_list()

    def reset_filter(self):
        self.update_list()

    def filter_by_tag(self):
        tag, ok = QInputDialog.getText(self, "タグで絞り込み", "タグ名を入力:")
        if ok:
            tasks = [t for t in self.todo_list.tasks if t.tag == tag]
            self.update_list(tasks, message=f"現在の表示：タグ「{tag}」")

    def filter_incomplete(self):
        tasks = [t for t in self.todo_list.tasks if not t.completed]
        self.update_list(tasks, message="現在の表示：未完了タスクのみ")

    def search_tasks(self):
        keyword, ok = QInputDialog.getText(self, "キーワード検索", "タイトルに含まれる文字:")
        if ok:
            tasks = [t for t in self.todo_list.tasks if keyword.lower() in t.title.lower()]
            self.update_list(tasks, message=f"現在の表示：「{keyword}」を含むタスク")

    def sort_by_due_date(self):
        self.todo_list.sort_by_due_date()
        self.update_list(message="現在の表示：締切日順")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())
