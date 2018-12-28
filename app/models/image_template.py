from sqlalchemy import Column, Integer, orm, Text

from app.models.base import Base


class ImageTemplate(Base):
	__tablename__ = "image_template"

	id = Column(Integer, primary_key=True)
	content = Column(Text)

	@orm.reconstructor
	def __init__(self):
		Base.__init__(self)
		self.fields = ['id', 'content']
