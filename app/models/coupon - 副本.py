from sqlalchemy import Column, Integer, String, BIGINT, ForeignKey, Table, orm
from sqlalchemy.orm import relationship

from app.libs.mytime import toNumTime
from app.models.base import Base, db
from app.models.description import Description
from app.models.images import Images
from app.models.seller import Seller
from app.models.url import Url

# 优惠卷表写图片表的中间表
coupon_images = Table(
    "coupon_images",
    Base.metadata,
    Column("coupon_id", Integer, ForeignKey("coupon.id"), nullable=False, primary_key=True),
    Column("image_id", Integer, ForeignKey("images.id"), nullable=False, primary_key=True)
)

class Coupon(Base):

	id = Column(Integer, primary_key=True)
	# 淘宝后台一级类目
	category_id = Column(Integer, nullable = False)
	# 商品ID
	num_iid = Column(BIGINT, nullable = False)
	# 商家ID，在seller表中的ID
	seller_id = Column(Integer, ForeignKey('seller.id'))
	# 商品标题
	title = Column(String(64), nullable = False)
	# 折扣价（原价）
	zk_final_price = Column(Integer, nullable = False)
	# 卷价格
	coupon_price = Column(Integer, nullable = False)
	# 优惠券面额信息
	coupon_info = Column(String(64), nullable = False)
	# 佣金比率(%)
	commission_rate = Column(Integer, nullable = False)
	# 30天销量
	volume = Column(Integer, nullable = False)
	# 商品主图
	pict_url_id = Column(Integer, ForeignKey('images.id'), nullable = False)
	# 淘口令
	token = Column(String(64), nullable = False)
	# 商品详情页链接地址
	item_url_id = Column(Integer, ForeignKey('url.id'))
	# 商品优惠券推广链接
	click_url_id = Column(Integer, ForeignKey('url.id'))
	# 优惠券总量
	total_count = Column(Integer, nullable = False)
	# 优惠券剩余量
	remain_count = Column(Integer, nullable = False)
	# 商品摘要
	description_id = Column(Integer, ForeignKey('description.id'))
	# 优惠券开始时间
	start_time = Column(Integer, nullable = False)
	# 优惠券结束时间
	end_time = Column(Integer, nullable = False)
	# 关联images模型
	pict_url = relationship('Images', foreign_keys=[pict_url_id])
	small_pic = relationship('Images', secondary=coupon_images)
	# 关联seller模型
	seller = relationship('Seller')
	# 关联description模型
	description = relationship('Description')
	# 关联url模型
	click_url = relationship('Url', foreign_keys=[click_url_id])
	item_url = relationship('Url', foreign_keys=[item_url_id])

	def __init__(self, data):
		self.category_id = data['category']
		self.num_iid = data['num_iid']
		self.title = data['title']
		self.zk_final_price = data['zk_final_price']
		self.coupon_price = data['coupon_price']
		self.coupon_info = data['coupon_info']
		self.commission_rate = data['commission_rate']
		self.volume = data['volume']
		self.token = data['token']
		self.total_count = data['coupon_total_count']
		self.remain_count = data['coupon_remain_count']
		self.start_time = toNumTime(data['coupon_start_time'])
		self.end_time = toNumTime(data['coupon_end_time'])

	def keys(self):
		return ['id', 'title', 'pict_url', 'num_iid', 'title']

	@staticmethod
	def create(data):
		''' 创建一个优惠卷 '''
		with db.auto_commit():
			# 先写入url表
			click_url = Url(data['coupon_click_url'])
			item_url = Url(data['item_url'])
			# 写入images表
			pict_url = Images(data['pict_url'])
			# 写入小图
			small_images_obj = []
			for pic in data['small_images']['string']:
				small_images_obj.append(Images(pic))
			# 写入商品摘要
			description = Description(data['item_description'])
			# 写入优惠卷信息
			coupon = Coupon(data)
			# 将url进行关联
			coupon.click_url = click_url
			coupon.item_url = item_url
			coupon.pict_url = pict_url
			coupon.small_pic = small_images_obj
			coupon.description = description
			# 写入商家信息,如果商家信息不存在则进行新增
			seller = Seller.query.filter_by(seller_id=data['seller_id']).first()
			if seller == None:
				seller = Seller(data['seller_id'], data['nick'], data['shop_title'], data['user_type'])
				coupon.seller = seller
			else:
				coupon.seller_id = seller.id
			db.session.add(coupon)

	@staticmethod
	def create_all(datas):
		err_list = []
		ok_list = []
		for data in datas:
			if (data['token'] == '') | (data['token'] == None):
				err_list.append(data['num_iid'])
				continue
			# 查找每条记录是否已经存在
			coupon = Coupon.query.filter_by(num_iid=data['num_iid']).first()
			if not coupon:
				Coupon.create(data)
			ok_list.append(data['num_iid'])
		return {'err': err_list, 'ok': ok_list}

	def __repr__(self):
		return '%s(%r)' % (self.__class__.__name__, self.title)