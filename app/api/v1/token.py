from flask import current_app, jsonify
from flask_cors import cross_origin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.libs.enums import ClientTypeEnum
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm


api = Redprint('token')

# 获取token
@api.route('', methods=['POST'])
@cross_origin()
def get_token():
    # 数据验证
    form = ClientForm().validate_for_api()
    # 选择对应的客户端类型进行用户验证
    pormise = {
        ClientTypeEnum.USER_EMAIL: User.verify
    }
    identity = pormise[form.type.data](form.account.data, form.secret.data)
    # 生成Token令牌
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identity['uid'], form.type.data, identity['scope'], expiration)
    t = {
        'token': token.decode('ascii')
    }
    return jsonify(t), 201


# 生成令牌
def generate_auth_token(uid, ac_type, scope=None, expiration=7200):
    """生成令牌"""
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'scope': scope
    })
