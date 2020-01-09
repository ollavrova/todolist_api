import pytz
from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields as mfields, post_load

ma = Marshmallow()
db = SQLAlchemy()


# Flask-SQLAlchemy model definitions
class TodoList(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now(pytz.utc))
    name = db.Column(db.String(150), unique=True, nullable=False)
    tasks = db.relationship('Task', backref=db.backref('todolist'), lazy=True)

    def __repr__(self):
        return '<TodoList {} from {}>'.format(self.name, self.timestamp)


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now(pytz.utc))
    name = db.Column(db.String(150))
    done = db.Column(db.Boolean(), default=False)
    todolist_id = db.Column(db.Integer, db.ForeignKey('todolist.id'), nullable=False)

    def __repr__(self):
        return '<Task {}>'.format(self.id)


class TaskSchema(Schema):
    id = mfields.Integer(dump_only=True)
    timestamp = mfields.DateTime()
    name = mfields.String(required=True)
    done = mfields.Boolean()
    todolist_id = mfields.Integer(required=True)

    @post_load
    def make_task(self, data, **kwargs):
        return Task(**data)


class TodoSchema(Schema):
    id = mfields.Integer()
    timestamp = mfields.DateTime()
    name = mfields.String(required=True)
    tasks = mfields.Nested(TaskSchema(many=True, exclude=['todolist_id']))

    @post_load
    def make_todo(self, data, **kwargs):
        return TodoList(**data)


class TaskDone(Schema):
    done = mfields.Boolean()

