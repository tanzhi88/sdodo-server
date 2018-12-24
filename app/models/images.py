from flask import current_app
from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Images(Base):
	id = Column(Integer, primary_key=True)
	_url = Column('url', String(255))
	img_from = Column(Integer)

	def __init__(self, url, img_from=1):
		self._url = url
		self.img_from = img_from

	def keys(self):
		return ['url']

	@property
	def url(self):
		"""
		设置图片地址，img_from为0则是本地图片
		"""
		url = self._url
		if self.img_from == 0:
			url = current_app.config['DOMAIN_STATIC'] + self._url
		return url
