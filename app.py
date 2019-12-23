from flask import Blueprint
from flask_restful import Api
from resources.task import TaskFinish, TaskAPI
from resources.todolist import TodoListAPI, TodoListTasks, TodoListAddTaskToList

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(TodoListAPI, '/todolists', '/todolists/<int:id>')
api.add_resource(TodoListAddTaskToList, '/todolists/<int:todolist_id>/add_task/<int:task_id>')
api.add_resource(TodoListTasks, '/todolists/<int:id>/tasks')
api.add_resource(TaskAPI, '/tasks', '/tasks/<int:id>')
api.add_resource(TaskFinish,  '/tasks/<int:id>/finish')
