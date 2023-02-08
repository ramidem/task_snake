from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': 'buy groceries',
        'description': 'milk, cheese',
        'done': False,
    },
    {
        'id': 2,
        'title': 'learn python using chat gpt',
        'description': 'YOLO',
        'done': False,
    },
]


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return jsonify({'message': 'No task found with id {}'.format(task_id)})
    return jsonify({'task': task[0]})


@app.route('/tasks', methods=['POST'])
def create_task():
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False,
    }

    tasks.append(task)

    return jsonify({'task': task}), 201


if __name__ == '__main__':
    app.run(debug=True)
