from flask import Flask, Blueprint, jsonify, request, redirect
from flasgger import Swagger

import sqlite3

app = Flask(__name__)
v1 = Blueprint('api/v1', __name__)
swagger = Swagger(app)


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


@v1.errorhandler(Exception)
def handle_error(error):
    status_code = 404
    if hasattr(error, 'code'):
        status_code = error.code
    return jsonify({"error": str(error)}), status_code


def not_found_error():
    error = Exception('Task not found')
    error.code = 404
    raise error


@v1.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Get a list of all tasks
    ---
    responses:
        200:
            description: A list of tasks
            schema:
                type: array
                items:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The task ID
                        task:
                            type: string
                            description: The task
                        done:
                            type: boolean
                            description: The task status
    """
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


@v1.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Get a task
    ---
    parameters:
      - in: path
        name: task_id
        type: number
    responses:
        200:
            description: A task
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        description: The task ID
                    task:
                        type: string
                        description: The task
                    done:
                        type: boolean
                        description: The task status
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id=?", [task_id])
    task = cursor.fetchone()

    if task is None:
        not_found_error()

    return jsonify({
        "id": task[0],
        "task": task[1],
        "done": task[2],
    }), 200


@v1.route('/tasks', methods=['POST'])
def create_task():
    """
    Create a task
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - task
          properties:
            task:
              type: string
              description: Task string
    responses:
        200:
            description: A task
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        description: The task ID
                    task:
                        type: string
                        description: The task
                    done:
                        type: boolean
                        description: The task status
    """
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


@v1.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update a task
    ---
    parameters:
      - name: task_id
        in: path
        type: number
        required: true
      - name: body
        in: body
        required: true
        schema:
          required:
            - task
          properties:
            task:
              type: string
              description: Task string
            done:
              type: number
              description: Status of the task
    responses:
        200:
            description: A task
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        description: The task ID
                    task:
                        type: string
                        description: The task
                    done:
                        type: boolean
                        description: The task status
    """
    new_task = request.get_json()['task']
    done = request.get_json()['done']

    conn = get_db()
    cursor = conn.cursor()

    existing_task = get_task(task_id)

    if existing_task is None:
        not_found_error()

    cursor.execute("UPDATE tasks SET task=?, done=? WHERE id=?",
                   [new_task, done, task_id])
    conn.commit()

    return get_task(task_id)


@v1.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a task
    ---
    parameters:
      - in: path
        name: task_id
        type: number
    responses:
        200:
            description: Confirmation message
            schema:
                type: object
                properties:
                    message:
                        type: string
                        description: Task deletion confirmation
    """
    conn = get_db()
    cursor = conn.cursor()

    task = get_task(task_id)

    if task is None:
        not_found_error()

    cursor.execute("DELETE FROM tasks WHERE id=?", [task_id])
    conn.commit()

    return jsonify({'message': 'Task deleted'})


app.register_blueprint(v1, url_prefix='/api/v1')


if __name__ == '__main__':
    app.run(debug=True)
