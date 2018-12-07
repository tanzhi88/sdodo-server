from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Seller(Base):
	"""docstring for Seller"""

	id = Column(Integer, primary_key=True)
	seller_id = Column(Integer)
	seller_nick = Column(String(255))
	shop_title = Column(String(255))
	shop_type = Column(Integer)

	def __init__(self, seller_id, seller_nick, shop_title, shop_type=0):
		self.seller_id = seller_id
		self.seller_nick = seller_nick
		self.shop_title = shop_title
		self.shop_type = shop_type

	def keys(self):
		return [
			'id',
			'seller_id',
			'seller_nick',
			'shop_title',
			'shop_type'
		]
