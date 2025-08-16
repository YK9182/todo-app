# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from todolist import ToDoList
from task import Task
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = 'your-secret-key'
todo_list = ToDoList()

def get_stats(tasks):
    total = len(tasks)
    completed = sum(1 for t in tasks if t.completed)
    overdue = sum(1 for t in tasks if t.is_overdue() and not t.completed)
    completion_rate = int((completed / total) * 100) if total > 0 else 0
    return {
        "total": total,
        "completed": completed,
        "overdue": overdue,
        "completion_rate": completion_rate
    }

@app.route('/')
def index():
    search = request.args.get('search', '').strip().lower()
    tag = request.args.get('tag', '')
    sort = request.args.get('sort', '')
    hide_completed = request.args.get('hide_completed') == '1'

    tasks = todo_list.tasks.copy()

    if search:
        tasks = [t for t in tasks if search in t.title.lower()]
    if tag:
        tasks = [t for t in tasks if t.tag == tag]
    if hide_completed:
        tasks = [t for t in tasks if not t.completed]
    if sort == 'due_date':
        tasks.sort(key=lambda t: t.get_due_datetime() or datetime.max)
    elif sort == 'title':
        tasks.sort(key=lambda t: t.title.lower())
    elif sort == 'completed':
        tasks.sort(key=lambda t: t.completed)

    all_tags = sorted({t.tag for t in todo_list.tasks if t.tag})
    stats = get_stats(todo_list.tasks)
    return render_template('index.html', 
                           tasks=tasks,
                           enumerate=enumerate,
                           stats=stats, 
                           all_tags=all_tags,
                           current_search=search, 
                           current_tag=tag,
                           today=date.today())

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title'].strip()
    if not title:
        flash("タイトルは必須です", "error")
        return redirect(url_for('index'))

    due_date = request.form.get('due_date', '')
    try:
        if due_date:
            datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        flash("日付の形式が正しくありません（例: 2024-12-31）", "error")
        return redirect(url_for('index'))

    description = request.form.get('description', '')
    tag = request.form.get('tag', '')
    priority = request.form.get('priority', 'medium')

    new_task = Task(title, description, due_date, False, tag, priority)
    todo_list.add_task(new_task)
    flash("タスクを追加しました", "success")
    return redirect(url_for('index'))

@app.route('/toggle/<int:index>')
def toggle_task(index):
    if index < 0 or index >= len(todo_list.tasks):
        flash("無効なタスク番号です", "error")
        return redirect(url_for('index'))
    todo_list.toggle_task(index)
    flash("完了状態を切り替えました", "info")
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete_task(index):
    if index < 0 or index >= len(todo_list.tasks):
        flash("無効なタスク番号です", "error")
        return redirect(url_for('index'))
    todo_list.delete_task(index)
    flash("タスクを削除しました", "success")
    return redirect(url_for('index'))

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_task(index):
    if index < 0 or index >= len(todo_list.tasks):
        flash("無効なタスク番号です", "error")
        return redirect(url_for('index'))
    task = todo_list.get_task(index)
    if request.method == 'POST':
        task.title = request.form['title'].strip()
        if not task.title:
            flash("タイトルは必須です", "error")
            return redirect(url_for('edit_task', index=index))

        task.description = request.form.get('description', '')
        task.due_date = request.form.get('due_date', '')
        task.tag = request.form.get('tag', '')
        task.priority = request.form.get('priority', 'medium')
        todo_list.save_to_file()
        flash("タスクを更新しました", "success")
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)

@app.route('/sort')
def sort_tasks():
    todo_list.sort_by_due_date()
    flash("締切日順に並び替えました", "info")
    return redirect(url_for('index'))

@app.route('/clear_completed')
def clear_completed():
    todo_list.tasks = [t for t in todo_list.tasks if not t.completed]
    todo_list.save_to_file()
    flash("完了済みタスクを削除しました", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
