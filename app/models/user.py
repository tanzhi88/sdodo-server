from flask import current_app
from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.enums import UserTypeEnum
from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db


class User(Base):
	id = Column(Integer, primary_key=True)
	email = Column(String(24), unique=True, nullable=False)
	nickname = Column(String(24), unique=True)
	avatar = Column(String(100))
	auth = Column(SmallInteger, default=1)
	_password = Column('password', String(100))
	_avatar = ''

	@orm.reconstructor
	def __init__(self):
		Base.__init__(self)
		self.fields = ['id', 'email', 'nickname', 'avatar_path']

	@property
	def avatar_path(self):
		return current_app.config['DOMAIN_STATIC'] + '/avatar/' + self.avatar

	@property
	def password(self):
		return self._password

	@password.setter
	def password(self, raw):
		self._password = generate_password_hash(raw)

	# 初始化超级管理员
	@staticmethod
	def init_super(nickname, account, secret):
		auth = 99
		super = User.query.filter_by(auth=auth).first()
		if not super:
			with db.auto_commit():
				user = User()
				user.nickname = nickname
				user.email = account
				user.password = secret
				user.auth = auth
				user.avatar = '1.png'
				db.session.add(user)
		else:
			raise AuthFailed()

	# 邮件的方式注册
	@staticmethod
	def register_by_email(nickname: object, account: object, secret: object) -> object:
		with db.auto_commit():
			user = User()
			user.nickname = nickname
			user.email = account
			user.password = secret
			user.avatar = '1.png'
			db.session.add(user)

	# 邮件方式验证用户
	@staticmethod
	def verify(email, password):
		# 在数据库中查找相应的用户，如果没有则直接在first_or_404中抛出异常，有则进行密码验证
		user = User.query.filter_by(email=email).first_or_404()
		if not user.check_password(password):
			raise AuthFailed()
		# 找到对应权限的名称
		scope = UserTypeEnum(user.auth).name
		return {'uid': user.id, 'scope': scope}

	# 验证密码
	def check_password(self, raw):
		if not self._password:
			return False
		return check_password_hash(self._password, raw)
