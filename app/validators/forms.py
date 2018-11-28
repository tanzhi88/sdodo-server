from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp
from wtforms import ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form

# 验证客户端传来的注册信息
class ClientForm(Form):
    account = StringField(validators=[DataRequired(), length(min=5, max=32)])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            # 此处尝试将传来的客户端类型找到相应的枚举类型，找不到则说明数据违法
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        # 将转成数字的客户端类型赋值给type，方便视图函数调用
        self.type.data = client

# 验证邮箱方式注册的信息
class UserEmailForm(ClientForm):
    account = StringField(validators=[Email(message='invalidate email')])
    secret = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')])
    nickname = StringField(validators=[DataRequired(), length(min=2, max=22)])

    # 检测账号是否重复
    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError('账号重复')