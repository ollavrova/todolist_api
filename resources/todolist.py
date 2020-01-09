from .task import tasks_schema
from models import TodoList, db, TodoSchema, Task
from flask import request
from flask_restful import Resource, fields


todo_schema = TodoSchema()
todolists_schema = TodoSchema(many=True)


class TodoListAPI(Resource):

    def get(self, pk=False):
        """
        get one by id or list of todolists
        :param pk: int, todolist id
        :return:
        """

        if pk:
            todolist = TodoList.query.get(pk)
            if not todolist:
                return {'status': 'error', 'message': 'Todolist is not found'}, 404
            data = todo_schema.dump(todolist)
            return {"status": "success", "todolist": data}, 200
        else:
            todolists = TodoList.query.all()
            if not todolists:
                return {"message": "Hello, todolists is empty yet!"}
            data = todolists_schema.dump(todolists)
            return {"status": "success", "todolists": data}, 200

    def post(self):
        """
        create an instance
        :return: created instance in json view, 201 status code
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        errors = todo_schema.validate(json_data)
        if errors:
            return errors, 422
        # Validate and deserialize input
        todolist = TodoList.query.filter_by(name=json_data['name']).first()
        if todolist:
            return {'message': 'Todolist already exists'}, 400
        todolist = TodoList(
            name=json_data['name']
        )
        db.session.add(todolist)
        db.session.commit()

        result = todo_schema.dump(todolist)

        return {"status": 'success', 'todolist': result}, 201


class TodoListTasks(Resource):
    """
    endpoint that show list of tasks by todolist_id
    """

    def get(self, pk):
        todolist = TodoList.query.get(pk)
        if not todolist:
            return {'status': 'error', 'message': 'Todolist for tasks list is not found'}, 400
        # Validate and deserialize input
        tasks = Task.query.filter_by(todolist_id=pk).all()
        data = tasks_schema.dump(tasks)
        return {'status': 'success', 'tasks': data}, 200


class TodoListAddTaskToList(Resource):

    def post(self, todolist_id, task_id):
        """
        custom method which allow to  add task to any todolist
        :param todolist_id: int
        :param task_id: int
        :return:
        """
        try:
            task = Task.query.get(task_id)
            if not task:
                return {'status': 'error', 'message': 'Task is not found'}, 400
        except:
            return {'status': 'error', 'message': 'Task is not found'}, 400

        try:
            todolist = TodoList.query.get(todolist_id)
            if not todolist:
                return {'status': 'error', 'message': 'Todolist is not found'}, 400
        except:
            return {'status': 'error', 'message': 'Todolist is not found'}, 400

        todolist.tasks.append(task)
        db.session.add(todolist)
        db.session.commit()

        result = todo_schema.dump(todolist)

        return {'status': "success", 'todolist': result, 'message': 'Task added to todo list!'}, 204
