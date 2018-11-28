from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'ac_type', 'scope'])

# 此方法为框架的接口验证的入口，凡是访问带有 @auth.login_required 装饰器的视图函数都会先进入此方法
@auth.verify_password
def verify_password(token, password):
    # 解密token获取用户信息，并将解密出来的用户信息存入g变量
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True

# 解密令牌
def verify_auth_token(token):
    # 实例一个序列
    s = Serializer(current_app.config['SECRET_KEY'])
    # 将传过来的token进行解密
    try:
        data = s.loads(token)
    # 捕捉异常，如果有异常说明token不正确
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    # 检查权限是否能访问此接口
    allow = is_in_scope(data['scope'], request.endpoint)
    if not allow:
        raise Forbidden()
    # 将解密出来的token信息转成namedtuple格式并返回
    return User(data['uid'], data['type'], data['scope'])