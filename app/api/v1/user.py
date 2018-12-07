from flask import jsonify, g, request

from app.libs.error_code import DeleteSuccess, Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.user import User

api = Redprint('user')

@api.route('/init', methods=['PUT'])
def init():
	data = request.json
	User.init_super(data['nickname'], data['account'], data['secret'])
	return Success()


# 获取用户(管理员可访问)
@api.route('/<int:uid>')
@auth.login_required
def admin_get_user(uid):
	user = User.query.get_or_404(uid)
	return jsonify(user)


# 获取用户(所有用户都可以访问)
@api.route('')
@auth.login_required
def get_user():
	uid = g.user.uid
	user = User.query.filter_by(id=uid).first_or_404()
	return jsonify(user)


# 删除用户(管理员可访问)
@api.route('/<int:uid>', methods=['DELETE'])
@auth.login_required
def delete_user(uid):
	with db.auto_commit():
		user = User.query.filter_by(id=uid).first_or_404()
		user.delete()
	return DeleteSuccess()


# 更新用户(所有用户都可以访问)
@api.route('', methods=['PUT'])
@auth.login_required
def update_user():
	data = request.json
	uid = g.user.uid
	user = User.query.get_or_404(uid)
	with db.auto_commit():
		user.nickname = data['nickname']
	return Success()


# 更新用户(管理员可访问)
@api.route('/<int:uid>', methods=['PUT'])
@auth.login_required
def admin_update_user():
	return 'update qiyue'


# 创建一个新的红图
users = Redprint('users')


# 获取用户列表
@users.route('')
@auth.login_required
def admin_get_users():
	user_list = User.query.all()
	return jsonify(user_list)
