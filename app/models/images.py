from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Images(Base):

	id = Column(Integer, primary_key=True)
	url = Column(String(255))
	img_from = Column(Integer)

	def __init__(self, url, img_from = 1):
		self.url = url
		self.img_from = img_from

	def keys(self):
		return ['url']