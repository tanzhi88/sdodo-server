from sqlalchemy import Integer, String, Column

from app.models.base import Base


class Description(Base):
	"""docstring for Url"""

	__tablename__ = 'description'

	id = Column(Integer, primary_key=True)
	content = Column(String(255))


	def __init__(self, content):
		self.content = content