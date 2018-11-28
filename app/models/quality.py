from flask import g
from sqlalchemy import Column, Integer, String, Table, ForeignKey, orm
from sqlalchemy.orm import relationship, backref

from app.libs.error_code import AuthFailed
from app.libs.mytime import toStrTime
from app.models.base import Base, db

quality_coupon = Table(
    "quality_coupon",
    Base.metadata,
    Column("quality_id", Integer, ForeignKey("quality.id"), nullable=False, primary_key=True),
    Column("coupon_id", Integer, ForeignKey("coupon.id"), nullable=False, primary_key=True)
)

class Quality(Base):
    ''' 精品库模型 '''

    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=None, nullable=False)
    user_id = Column(Integer, nullable=False)
    coupon = relationship('Coupon', secondary=quality_coupon, lazy=True, backref=backref('quality', lazy=True))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'title', 'user_id', 'coupon']

    # def keys(self):
    #     return ['id', 'title', 'coupon']

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
    def put_item_in_quality(qid, items):
        ''' 将优惠卷写入精品库 '''
        quality = Quality.query.filter_by(id=qid).first_or_404()
        for item in items:
            pass



