Example api project
=================
Simple TODO list app API with python flask and a SQL backend.
Used - python3.6, flask, flask_restful, flask_testing, Sqlite, SQLAlchemy, Flask Blueprints

Application allows:  
- Create multiple TODO lists.
- Add a task to the TODO list.
- Get all tasks from one TODO list.
- Delete task.
- Edit task.
- Finish task.

Work:
========
Clone a project, go to the project folder. Create a virtual environment, install requirements :
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create databade:
```bash
python migrate.py db init
python migrate.py db migrate
python migrate.py db upgrade

```

and run project by a command:
```bash

python run.py
```

Testing:
=======
```
python tests.py
```

API Endpoints:
=========
- GET http://127.0.0.1:5000/api/todolists - list of todo lists
- POST http://127.0.0.1:5000/api/todolists - create a todo list
- GET http://127.0.0.1:5000/todolists/<int:id>  - get one todo list by id
- POST http://127.0.0.1:5000/todolists/<int:todolist_id>/add_task/<int:task_id> - add task by task_id to todo list with todolist_id
- GET http://127.0.0.1:5000/todolists/<int:id>/tasks - get list of tasks for todo list with todolist_id
- GET  http://127.0.0.1:5000/api/tasks - list of all tasks
- POST  http://127.0.0.1:5000/api/tasks - create a task
- GET http://127.0.0.1:5000/tasks/<int:id> - get one task by task_id
- PUT http://127.0.0.1:5000/tasks/<int:id> - edit one task by task_id
- DELETE http://127.0.0.1:5000/tasks/<int:id> - delete one task by task_id
- PUT http://127.0.0.1:5000/tasks/<int:id>/finish - mark task finished


Example of commands for testing:
- you can use curl or python requests package

$ python3
import requests
requests.get('http://127.0.0.1:5000/api/todolists')
or

MIMETYPE="application/json"
HOST=127.0.0.1:5000
curl -H "Accept: $MIMETYPE" -H "Content-Type: $MIMETYPE" http://$HOST/api/todolist -X POST -d '{"name":"1234"}'
```bash
{
    "status": "success",
    "todolists": [
        {
            "name": "First list",
            "timestamp": "2019-12-23T12:04:55.897879",
            "id": 1,
            "tasks": [
                {
                    "id": 1,
                    "timestamp": "2019-12-23T12:04:55.901860",
                    "name": "First task",
                    "done": true
                },
                {
                    "id": 2,
                    "timestamp": "2019-12-23T12:04:55.901860",
                    "name": "Second task",
                    "done": false
                },
                {
                    "id": 3,
                    "timestamp": "2019-12-23T12:04:55.901860",
                    "name": "Third task",
                    "done": false
                }
            ]
        },
        {
            "name": "Second todo list",
            "timestamp": "2019-12-23T12:04:55.897879",
            "id": 2,
            "tasks": []
        }
    ]
}
```

$ curl -H "Accept: $MIMETYPE" -H "Content-Type: $MIMETYPE" http://$HOST/api/todolists/1
```bash
{
    "status": "success",
    "todolist": {
        "name": "First list",
        "timestamp": "2019-12-23T12:04:55.897879",
        "id": 1,
        "tasks": [
            {
                "id": 1,
                "timestamp": "2019-12-23T12:04:55.901860",
                "name": "First task",
                "done": true
            },
            {
                "id": 2,
                "timestamp": "2019-12-23T12:04:55.901860",
                "name": "Second task",
                "done": false
            },
            {
                "id": 3,
                "timestamp": "2019-12-23T12:04:55.901860",
                "name": "Third task",
                "done": false
            }
        ]
 ```   
 

$ curl -H "Accept: $MIMETYPE" -H "Content-Type: $MIMETYPE" http://$HOST/api/todolists/1/tasks
```bash
{
    "status": "success",
    "tasks": [
        {
            "todolist_id": 1,
            "name": "First task",
            "id": 1,
            "done": true,
            "timestamp": "2019-12-23T12:04:55.901860"
        },
        {
            "todolist_id": 1,
            "name": "Second task",
            "id": 2,
            "done": false,
            "timestamp": "2019-12-23T12:04:55.901860"
        },
        {
            "todolist_id": 1,
            "name": "Third task",
            "id": 3,
            "done": false,
            "timestamp": "2019-12-23T12:04:55.901860"
        }
    ]
}
```

$ curl -H "Accept: $MIMETYPE" -H "Content-Type: $MIMETYPE" http://$HOST/api/tasks
```bash

{
    "status": "success",
    "tasks": [
        {
            "todolist_id": 1,
            "name": "First task",
            "id": 1,
            "done": true,
            "timestamp": "2019-12-23T12:04:55.901860"
        },
        {
            "todolist_id": 1,
            "name": "Second task",
            "id": 2,
            "done": false,
            "timestamp": "2019-12-23T12:04:55.901860"
        },
        {
            "todolist_id": 1,
            "name": "Third task",
            "id": 3,
            "done": false,
            "timestamp": "2019-12-23T12:04:55.901860"
        }
    ]
}
```
Get task, id=1

$ curl -H "Accept: $MIMETYPE" -H "Content-Type: $MIMETYPE" http://$HOST/api/tasks/1
```bash

{
    "status": "success",
    "task": {
        "todolist_id": 1,
        "name": "First task",
        "id": 1,
        "done": true,
        "timestamp": "2019-12-23T12:04:55.901860"
    }
}
```
create a task

$ curl -H "Accept: $MIMETYPE" -H "Content-Type: $MIMETYPE" $HOST/api/tasks -X POST -d '{"name":"654654", "todolist_id":"2"}'
```bash{
    "status": "success",
    "task": {
        "todolist_id": 2,
        "name": "654654",
        "id": 4,
        "done": false,
        "timestamp": "2019-12-23T12:06:50.150730"
    }
}

```
Edit task:
curl -H "Accept: $MIMETYPE" -H "Content-Type: $MIMETYPE" $HOST/api/tasks/4 -X PUT -d '{"name":"11111", "todolist_id":"2"}'

checking:
$ curl -H "Accept: $MIMETYPE" -H "Content-Type: $MIMETYPE" $HOST/api/tasks/4 
```{
    "status": "success",
    "task": {
        "todolist_id": 2,
        "name": "11111",
        "id": 4,
        "done": false,
        "timestamp": "2019-12-23T12:06:50.150730"
    }
}
```
Delete task

$ curl -H "Accept: $MIMETYPE" -H "Content-Type: $MIMETYPE" $HOST/api/tasks/4 -X DELETE
checking:
$ curl -H "Accept: $MIMETYPE" -H "Content-Type: $MIMETYPE" $HOST/api/tasks/4 
```bash{
    "status": "error",
    "message": "Task not found"
}
```
add task to todolist - 
 
you can edit task's todolist_id by PUT request or use special endpoint

$ curl -H "Accept: $MIMETYPE" -H "Content-Type: $MIMETYPE" $HOST/api/todolists/1/add_task/4 -X POST -d '{"name":"new task", "todolist_id":"2"}'
checking:
$ curl -H "Accept: $MIMETYPE" -H "Content-Type: $MIMETYPE" $HOST/api/todolists/1
```bash
{
    "status": "success",
    "todolist": {
        "name": "First list",
        "timestamp": "2019-12-23T12:04:55.897879",
        "id": 1,
        "tasks": [
            {
                "id": 1,
                "timestamp": "2019-12-23T12:04:55.901860",
                "name": "First task",
                "done": true
            },
            {
                "id": 2,
                "timestamp": "2019-12-23T12:04:55.901860",
                "name": "Second task",
                "done": false
            },
            {
                "id": 3,
                "timestamp": "2019-12-23T12:04:55.901860",
                "name": "Third task",
                "done": false
            },
            {
                "id": 4,
                "timestamp": "2019-12-23T12:06:50.150730",
                "name": "new task",
                "done": false
            }
        ]
    }
}
```
Mark task as finished - you can edit task's 'done' attribute by PUT request or use special endpoint:

$ curl -H "Accept: $MIMETYPE" -H "Content-Type: $MIMETYPE" $HOST/api/tasks/4/finish -X PUT -d '{"done":"True"}'

checking:

$ curl -H "Accept: $MIMETYPE" -H "Content-Type: $MIMETYPE" $HOST/api/tasks/4

```bash
{
    "status": "success",
    "task": {
        "todolist_id": 1,
        "name": "new task",
        "id": 4,
        "done": true,
        "timestamp": "2019-12-23T12:06:50.150730"
    }
}


```



