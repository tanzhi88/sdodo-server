from sqlalchemy import Column, Integer, String

from app.models.base import Base

class Url(Base):
	"""docstring for Url"""

	id = Column(Integer, primary_key=True)
	url = Column(String(255))

	def __init__(self, url):
		self.url = url