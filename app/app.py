from datetime import date
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from app.libs.error import ServerError
from bson.objectid import ObjectId


class JSONEncoder(_JSONEncoder):
    # default是递归调用的，只要是不能直接被python序列化的对象都会当成o传进来
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, ObjectId):
            return str(o)
        # logs
        raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder



