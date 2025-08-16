# ToDoリストアプリ集

このプロジェクトは、学習の一環として開発した **ToDoリストアプリ** です。  
Pythonを用いて、以下の2種類の形態で実装しています。

- Flask を使った **Webアプリ版**
- PyQt を使った **GUIデスクトップ版**

共通して JSON ファイルにデータを保存し、アプリを終了してもタスクが保持される仕組みになっています。  
異なる実装方式を通じて、バックエンド処理、データ管理、UI設計を学びました。

---

## 実装一覧

### 1. Webアプリ版（Flask）

- **ブラウザから操作できるToDoリスト**
- **UI**: Bootstrap + Font Awesome
- **画面構成**:
  - `templates/index.html`: メイン画面（タスク一覧、追加、検索、フィルター）
  - `templates/edit.html`: 編集画面（タスクの更新、状態表示）

**機能**:
- タスクの追加（タイトル・説明・期限・タグ・優先度）
- タスクの編集・削除
- 完了状態の切り替え
- 完了済みタスクの一括削除
- 検索、タグ絞り込み
- 並び替え（期限順、タイトル順、完了状況順）
- 統計表示（総数、完了数、達成率、期限切れ件数）
- 編集画面では「現在の状態（完了/未完了、優先度、期限切れまでの日数など）」を視覚的に表示

**起動方法**:
```
bash
cd flask_app
pip install -r requirements.txt   # Flask>=2.3
python app.py
```
# ブラウザで http://127.0.0.1:5000 にアクセス
2. GUIアプリ版（PyQt）
デスクトップアプリとして起動

UI: PyQt5 を利用

操作方法:

フォーム入力でタスクを追加

右クリックのコンテキストメニューから「完了切り替え」「削除」「編集」

ボタン操作でタグ絞り込み・未完了表示・検索・期限順ソート

機能:

タスク追加・編集・削除

タグでの絞り込み

未完了タスクのみ表示

キーワード検索

締切日順にソート

完了済みタスクは灰色＋取り消し線で表示

起動方法:

bash
コピーする
編集する
cd pyqt_app
pip install -r requirements.txt   # PyQt5==5.15.11
python todo_PyQt.py
データ保存
各アプリごとに独自の tasks.json を保持しています

Flask版: flask_app/tasks.json

PyQt版: pyqt_app/tasks.json

JSON形式でタスクを永続化

保存される情報: タイトル・説明・期限・タグ・優先度・完了状態

Flask版ではさらに「作成日時」「完了日時」も記録

ディレクトリ構成
bash
コピーする
編集する
.
├── flask_app/               # Flask版 Webアプリ
│   ├── app.py
│   ├── todolist.py
│   ├── task.py
│   ├── tasks.json
│   ├── requirements.txt
│   └── templates/
│       ├── index.html
│       └── edit.html
│
├── pyqt_app/                # PyQt版 GUIアプリ
│   ├── todo_PyQt.py
│   ├── todolist.py
│   ├── task.py
│   ├── tasks.json
│   └── requirements.txt
│
└── images/                  # スクリーンショット
    ├── web_list.png
    ├── web_add.png
    ├── web_edit.png
    ├── pyqt_list.png
    ├── pyqt_add.png
    └── pyqt_menu.png
スクリーンショット
Web版（Flask）
タスク一覧画面

タスク追加フォーム

編集画面

GUI版（PyQt）
メイン画面（タスク一覧表示）

タスク追加後（色付きタグ表示）

右クリックメニュー表示

学習の目的
PythonによるWebアプリとデスクトップアプリ開発の基礎習得

データ保存や状態管理をアプリごとに独立させて実装

フロントエンドとバックエンドの接続方法を学習

ポートフォリオとしてプログラミングスキルを可視化すること
