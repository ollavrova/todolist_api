import json
import unittest
from flask import Flask
from app import api_bp
from config import TestConfig
from models import db
from flask_testing import TestCase


def create_test_app():
    app = Flask(__name__)
    app.config.from_object(TestConfig)
    app.register_blueprint(api_bp, url_prefix='/api')
    db.init_app(app)
    app.app_context().push()
    return app


class TestCase(TestCase):
    headers = {
                'Accept': 'application/vnd.api+json',
                'Content-Type': 'application/vnd.api+json'
            }

    def create_app(self):
        return create_test_app()

    def setUp(self):
        app = create_test_app()
        db.init_app(app)
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_endpoints(self):
        response = self.client.get('/api/todolists')
        assert response.status_code == 200
        assert "Hello, todolists is empty yet!" in response.json['message']

        response = self.client.get('/api/tasks')
        assert response.status_code == 200
        assert "Hello, tasks are not created yet!" in response.json['message']

    def test_all(self):
        # create a todolist
        data = {"name": "First list"}
        response = self.client.post('/api/todolists', data=json.dumps(data), headers=self.headers)
        assert response.status_code == 201
        # assert "First list" in response.json.get('data')['name']
        todo = response.json.get('todolist')
        assert "First list" in todo['name']

        # check /todolists/id endpoint
        response = self.client.get('/api/todolists/'+str(todo['id']))
        assert response.status_code == 200
        assert 'todolist' in response.json
        assert response.json.get('todolist') == todo

        # create second todolist
        data = {"name": "Second todo list"}
        response = self.client.post('/api/todolists', data=json.dumps(data), headers=self.headers)
        assert response.status_code == 201
        todo2 = response.json.get('todolist')
        assert "Second todo list" in todo2['name']

        # create task
        data = {"name": "First task", "todolist_id": '1'}
        response = self.client.post('api/tasks', data=json.dumps(data), headers=self.headers)
        assert response.status_code == 201
        assert 'task' in response.json
        task = response.json['task']
        assert task['name'] == data['name']

        # create second task
        data = {"name": "Second task", "todolist_id": '2'}
        response = self.client.post('api/tasks', data=json.dumps(data), headers=self.headers)
        assert response.status_code == 201
        assert 'task' in response.json
        task2 = response.json['task']
        assert task2['name'] == data['name']

        # create third task
        data = {"name": "Third task", "todolist_id": '1'}
        response = self.client.post('api/tasks', data=json.dumps(data), headers=self.headers)
        assert response.status_code == 201
        assert 'task' in response.json
        task3 = response.json['task']
        assert task3['name'] == data['name']

        # check /todolists/<id>/tasks
        response = self.client.get('api/todolists/'+str(todo['id'])+'/tasks', headers=self.headers)
        assert response.status_code == 200
        assert task in response.json['tasks']
        assert task2 not in response.json['tasks']

        response = self.client.get('api/todolists/' + str(todo2['id']) + '/tasks', headers=self.headers)
        assert response.status_code == 200
        assert task2 in response.json['tasks']
        assert task not in response.json['tasks']

        # check /tasks/
        response = self.client.get('api/tasks', headers=self.headers)
        assert response.status_code == 200
        assert task in response.json['tasks']
        assert task2 in response.json['tasks']

        # check /tasks/<id>
        response = self.client.get('api/tasks/' + str(task['id']), headers=self.headers)
        assert response.status_code == 200
        assert response.json['task'] == task
        assert response.json['task'] != task2

        # check /todolists/ endpoint content
        todo1 = (self.client.get('/api/todolists/1')).json['todolist']
        todo2 = (self.client.get('/api/todolists/2')).json['todolist']
        task1 = (self.client.get('/api/tasks/1')).json['task']

        task2 = (self.client.get('/api/tasks/2')).json['task']
        task3 = (self.client.get('/api/tasks/3')).json['task']
        # task1.pop('todolist_id', None)
        del task1['todolist_id']
        del task2['todolist_id']
        del task3['todolist_id']
        response = self.client.get('/api/todolists')
        assert response.status_code == 200
        assert 'todolists' in response.json

        todolists = response.json['todolists']
        assert todo1 in todolists
        assert todo2 in todolists
        assert task1 in todolists[0]['tasks']
        assert task3 in todolists[0]['tasks']
        assert task2 not in todolists[0]['tasks']

        assert task2 in todolists[1]['tasks']
        assert task1 not in todolists[1]['tasks']
        assert task3 not in todolists[1]['tasks']

        # test finish task
        assert task1['done'] is False
        data = {'done': True}
        response = self.client.put('/api/tasks/'+str(task1['id'])+'/finish', data=json.dumps(data), headers=self.headers)
        assert response.status_code == 204

        response = self.client.get('/api/tasks/'+str(task1['id']), headers=self.headers)
        assert response.json['task']['id'] == task1['id']
        assert response.json['task']['done'] is True

        # check TaskAddToList post /todolists/<int:todolist_id>/add_task/<int:task_id>
        # let's add task2 to todo1
        response = self.client.post('/api/todolists/'+str(todo1['id'])+'/add_task/'+str(task2['id']),
                                    data=json.dumps(data),
                                    headers=self.headers)
        assert response.status_code == 204
        todo1 = (self.client.get('/api/todolists/1')).json['todolist']
        task2 = (self.client.get('/api/tasks/2')).json['task']
        assert task2['todolist_id'] == 1
        del task2['todolist_id']
        assert task2 in todo1['tasks']

        # test editing task
        task2 = (self.client.get('/api/tasks/2')).json['task']
        data = {"name": "Just other name", "todolist_id": task2['todolist_id']}
        response = self.client.put('/api/tasks/'+str(task2['id']), data=json.dumps(data), headers=self.headers)
        assert response.status_code == 204
        task2 = (self.client.get('/api/tasks/2')).json['task']
        assert task2['name'] == data['name']

        # test delete task
        task2 = (self.client.get('/api/tasks/2')).json['task']
        response = self.client.delete('/api/tasks/'+str(task2['id']), headers=self.headers)
        assert response.status_code == 204


if __name__ == '__main__':
    unittest.main()
