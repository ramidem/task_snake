from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      task TEXT,
      done BOOLEAN DEFAULT 0
    )
    """)

    return conn


@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    print(tasks)
    tasks_list = []
    for task in tasks:
        task_dict = {
            "id": task[0],
            "task": task[1],
            "done": task[2],
        }
        tasks_list.append(task_dict)

    return jsonify(tasks_list)


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id=?", [task_id])
    task = cursor.fetchone()

    task_dict = {
        "id": task[0],
        "task": task[1],
        "done": task[2],
    }

    return jsonify(task_dict)


@app.route('/tasks', methods=['POST'])
def create_task():
    task = request.get_json()['task']

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (task) VALUES (?)", [task])
    conn.commit()

    cursor.execute("SELECT * FROM tasks ORDER BY id DESC LIMIT 1")
    new_task = cursor.fetchone()

    task_dict = {
        "id": new_task[0],
        "task": new_task[1],
        "done": new_task[2],
    }

    return jsonify(task_dict), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = request.get_json()['task']
    done = request.get_json()['done']

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET task=?, done=? WHERE id=?",
                   [task, done, task_id])
    conn.commit()

    return get_task(task_id)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", [task_id])
    conn.commit()

    return jsonify({'message': 'Task deleted'})


if __name__ == '__main__':
    app.run(debug=True)
