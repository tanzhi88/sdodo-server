from flask import g
from sqlalchemy import Column, Integer, String, Table, ForeignKey, orm
from sqlalchemy.orm import relationship, backref

from app.libs.error_code import AuthFailed
from app.libs.mytime import toStrTime
from app.models.base import Base, db
from app.models.coupon import Coupon

quality_coupon = Table(
	"quality_coupon",
	Base.metadata,
	Column(
		"quality_id",
		Integer,
		ForeignKey("quality.id"),
		nullable=False,
		primary_key=True),
	Column(
		"coupon_id",
		Integer,
		ForeignKey("coupon.id"),
		nullable=False,
		primary_key=True))


class Quality(Base):
	''' 精品库模型 '''

	id = Column(Integer, primary_key=True)
	title = Column(String(255), unique=None, nullable=False)
	user_id = Column(Integer, nullable=False)
	r_coupon = relationship('Coupon', secondary=quality_coupon, lazy='dynamic',
	                        backref=backref('_quality', lazy='dynamic'))
	_coupon = {}

	@orm.reconstructor
	def __init__(self):
		Base.__init__(self)
		self.fields = ['id', 'title', 'user_id', 'create_time', 'create_time_str']

	@property
	def coupon(self):
		"""
		@property装饰器就是负责把一个方法变成属性调用
		@property本身又创建了另一个装饰器@coupon.setter，负责把一个setter方法变成属性赋值
		"""
		return self._coupon

	@coupon.setter
	def coupon(self, limit):
		coupon_list = self.r_coupon.order_by(Coupon.id.desc()).limit(limit).all()
		total = self.r_coupon.count()
		self._coupon = {'list': coupon_list, 'total': total}

	@property
	def create_time_str(self):
		"""
		创建一个方法属性，返回一个被格式化后的创建时间
		"""
		return toStrTime(self.create_time)

	@staticmethod
	def create_quality(title=''):
		''' 创建一个精品库 '''
		with db.auto_commit():
			quality = Quality()
			if title == '':
				title = '创建于' + toStrTime(0, '%Y-%m-%d %H:%M:%S')
			quality.title = title
			# 写入用户ID
			quality.user_id = g.user.uid
			db.session.add(quality)

	@staticmethod
	def save_quality(id, title=''):
		''' 修改一个精品库 '''
		with db.auto_commit():
			quality = Quality.query.filter_by(id=id).first_or_404()
			if quality.user_id != g.user.uid:
				raise AuthFailed()
			if title == '':
				title = '修改于' + toStrTime(0, '%Y-%m-%d %H:%M:%S')
			quality.title = title

	@staticmethod
	def put_item_in_quality(qid, coupons_dict):
		"""
		将优惠卷写入精品库
		先查出原有的商品，再将需要加入的商品新增，最后进行对比排除重复再新增
		:param qid: 精品库ID
		:param coupons_dict: 商品列表，每个商品为字典格式
		:return: 返回商品新增时成功和失败的数量字典
		"""
		quality = Quality.query.filter_by(id=qid).first_or_404()
		# 找出原有的coupon
		coupons = quality.r_coupon.all()
		# 将商品入库，并返回成功入库的商品的num_iid，在result['ok']中
		result = Coupon.create_all(coupons_dict)
		# 查询出所有num_iid的商品
		new_coupons = Coupon.query.filter(
			Coupon.num_iid.in_(result['ok'])).all()
		# 循环将未加入过的coupon追加到原来的coupons列表中
		for coupon in new_coupons:
			if not quality.r_coupon.filter_by(id=coupon.id).first():
				coupons.append(coupon)
		# 提交
		with db.auto_commit():
			quality.r_coupon = coupons
			db.session.add(quality)
		return result

	@staticmethod
	def quality_all(page=1, size=20):
		"""
		分页获取精品库列表
		:param page: 当前页
		:param size: 每页数量
		:return: 返回精品库列表，并且每个精品库带4个商品
		"""
		quality_o = Quality.query.filter_by().order_by(Quality.id.desc())
		# 如果不是超级管理员则只能获取自己的精品库
		if g.user.scope != 'SuperScope':
			quality_o = quality_o.filter_by(user_id=g.user.uid)
		# 进行分页获取
		quality_list = quality_o.limit(size).offset((page - 1) * size).all()
		# 循环获取每个精品库下的商品并追加到精品库上
		for quality in quality_list:
			# coupon的获取已经定义在属性方法中,这里通过设置属性值来控制要取出coupon的条数
			quality.coupon = 4
			quality.append('coupon')

		return {'quality_list': quality_list, 'total': quality_o.count()}

	@staticmethod
	def quality_get(qid, page=1, size=10):
		"""
		获取一个精品库的数据，并分页获取精品库下的商品列表
		:param qid: 精品库的ID
		:param page: 要获取当前页的页码
		:param size: 每页获取的数量
		:return: 将商品列表、商品总数追加到精品库对象中返回
		"""

		# 超级管理员可以查看所有精品库，反之只能查看自己的精品库
		if g.user.scope == 'SuperScope':
			quality = Quality.query.filter_by(id=qid).first_or_404()
		else:
			quality = Quality.query.filter_by(
				user_id=g.user.uid, id=qid).first_or_404()
		coupon_list = quality.r_coupon
		# 分页获取coupon数据
		quality.coupon_list = coupon_list.limit(
			size).offset((page - 1) * size).all()
		# coupon的总条数
		quality.coupon_total = coupon_list.count()
		quality.append('coupon_list', 'coupon_total')
		return quality
