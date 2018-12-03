from flask import request, jsonify, g

from app.libs.error_code import Success, DeleteSuccess
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.coupon import Coupon
from app.models.quality import Quality

api = Redprint('quality')


@api.route('')
@auth.login_required
def get_quality_list():
	''' 获取精品库列表 '''
	qualitys = Quality.query.filter_by(
		user_id=g.user.uid).order_by(
		Quality.id.desc()).all()
	return jsonify(qualitys)


@api.route('/<int:id>')
@auth.login_required
def get_coupon_by_quality(id):
	''' 获取一个精品库里的商品 '''
	quality = Quality.query.filter_by(user_id=g.user.uid, id=id).first_or_404()
	return jsonify(quality)


@api.route('', methods=['PUT'])
@auth.login_required
def add_quality():
	''' 新建一个精品库 '''
	data = request.json
	Quality.create_quality(data['title'])
	return Success()


@api.route('/<int:id>', methods=['POST'])
@auth.login_required
def save_quality(id):
	''' 编辑一个精品库 '''
	data = request.json
	Quality.save_quality(id, data['title'])
	return Success()


@api.route('/stock', methods=['POST'])
@auth.login_required
def put_item_in_quality():
	''' 选产品入库 '''
	data = request.json
	# 先检查是否存在精品库
	quality = Quality.query.filter_by(id=data['quality_id']).first_or_404()

	# 将商品入库，并返回成功入库的商品的num_iid，在result['ok']中
	result = Coupon.create_all(data['coupons'])
	# 查询出所有num_iid的商品，加入到quality中再提交
	coupons = Coupon.query.filter(Coupon.num_iid.in_(result['ok'])).all()
	with db.auto_commit():
		quality.coupon = coupons
		db.session.add(quality)

	return Success()


@api.route('/stock', methods=['DELETE'])
@auth.login_required
def put_item_out_quality():
	''' 移出精品库 '''
	data = request.json
	# 先检查是否存在精品库
	quality = Quality.query.filter_by(id=data['quality_id']).first_or_404()

	# 查找出
	coupons = Coupon.query.filter(Coupon.id.in_(data['coupon_id'])).all()
	with db.auto_commit():
		[quality.coupon.remove(coupon) for coupon in coupons]
	return Success()


@api.route('/<int:id>', methods=['DELETE'])
@auth.login_required
def del_quality(id):
	user = g.user
	with db.auto_commit():
		if user.scope == 'SuperScope':
			quality = Quality.query.get_or_404(id)
		else:
			quality = Quality.query.filter_by(id=id, user_id=user.uid).first_or_404()
		quality.delete()
	return DeleteSuccess()
