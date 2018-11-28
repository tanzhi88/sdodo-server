from datetime import date

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from app.libs.error_code import ServerError

# 新建json对象，改写default函数用来序列化对象
class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ServerError()

# 生成一个新的Flask核心对象，继承真正的Flask核心对象，用来改写json_encoder
class Flask(_Flask):
    json_encoder = JSONEncoder
