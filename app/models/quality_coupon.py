# from sqlalchemy import Table, Column, Integer, ForeignKey
#
# from app.models.base import Base
#
#
# quality_coupon = Table(
#     "quality_coupon",
#     Base.metadata,
#     Column("quality_id", Integer, ForeignKey("quality.id"), nullable=False, primary_key=True),
#     Column("coupon_id", Integer, ForeignKey("coupon.id"), nullable=False, primary_key=True)
# )
