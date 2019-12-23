from models import TodoList, Task, db, TaskSchema, TaskDone
from flask import request
from flask_restful import Resource


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
task_done = TaskDone()


class TaskAPI(Resource):

    def get(self, id=False):
        """
        get one by id or list of tasks
        :param id: int, task id
        :return:
        """
        if id:
            task = Task.query.get(id)
            if not task:
                return {'status': 'error', 'message': 'Task not found'}, 400
            data = task_schema.dump(task)
            return {"status": "success", "task": data}, 200
        else:
            tasks = Task.query.all()
            if not tasks:
                return {"message": "Hello, tasks are not created yet!"}
            data = tasks_schema.dump(tasks)
        return {"status": "success", "tasks": data}, 200

    def post(self):
        """
        create an instance of task
        :return: created instance in json view, status code 201
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        errors = task_schema.validate(json_data)
        if errors:
            return errors, 422
        # Validate and deserialize input
        data = task_schema.load(json_data)
        todolist_id = TodoList.query.filter_by(id=data.todolist_id).first()
        if not todolist_id:
            return {'status': 'error', 'message': 'Todolist for task not found'}, 400
        task = Task(
            todolist_id=data.todolist_id,
            name=data.name
        )
        db.session.add(task)
        db.session.commit()

        result = task_schema.dump(task)

        return {'status': "success", 'task': result}, 201

    def put(self, id):
        """
        editing of task
        :param id: task id
        :return: saved instance and status code 204
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        errors = task_schema.validate(json_data)
        if errors:
             return errors, 422
        data = task_schema.load(json_data)
        task = Task.query.get(id)
        if not task:
            return {'message': 'Task does not exist'}, 400
        todolist = TodoList.query.filter_by(id=data.todolist_id).first()
        if not todolist:
            return {'status': 'error', 'message': 'Todolist for task not found'}, 400
        task.todolist_id = todolist.id
        task.name = json_data['name'] if json_data.get('name') else task.name
        task.done = json_data['done'] if json_data.get('done') else task.done
        db.session.add(task)
        db.session.commit()
        result = task_schema.dump(task)
        return {"status": 'success', 'task': result}, 204

    def delete(self, id):
        """
        delete a task
        :param id: task id
        :return:
        """
        task = Task.query.get(id)
        if not task:
            return {'message': 'Task does not exist'}, 400
        db.session.delete(task)
        db.session.commit()
        result = task_schema.dump(task)
        return {"status": 'success', 'task': result}, 204


class TaskFinish(Resource):

    def put(self, id):
        """
        custom method which allow to mark task done
        :param id: task_id
        :return:
        """
        task = Task.query.get(id)
        if not task:
            return {'status': 'error', 'message': 'Task not found'}, 400
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        errors = task_done.validate(json_data)
        if errors:
            return errors, 422
        data = task_done.load(json_data)
        task.done = True
        db.session.add(task)
        db.session.commit()

        result = task_done.dump(task)

        return {'status': "success", 'task': result}, 204
