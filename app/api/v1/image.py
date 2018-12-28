from flask import current_app, request, jsonify

from app.libs.ci import CreatedImage
from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.coupon import Coupon
from app.models.image_template import ImageTemplate

api = Redprint('image')


@api.route('', methods=['PUT'])
@auth.login_required
def created_image():
	"""
	生成图片
	:return:
	"""
	img_data = request.json
	# 1、先确定图保存路径
	static_path = current_app.config['STATIC_PATH']
	file_name = 'img/' + img_data['base']['file']
	file = static_path + file_name
	# 2、创建图片
	ci = CreatedImage(file, img_data['items'], img_data['base']['size'])
	ci.draw()
	ci.save()
	# 3、保存入数据库
	Coupon.add_publicize_img(img_data['base']['id'], file_name)
	return Success()


@api.route('/more', methods=['PUT'])
@auth.login_required
def created_image_more():
	data = request.json
	static_path = current_app.config['STATIC_PATH']
	template_path = static_path + 'template/'
	save_path = static_path + 'img/'
	coupons = Coupon.query.filter(Coupon.id.in_(data['coupon_ids'])).all()
	for coupon in coupons:
		ci = CreatedImage(coupon, data['url'], template_path, save_path)
		ci.save()
	return Success()


@api.route('/template')
@auth.login_required
def get_template():
	tid = request.args.get('tid', None)
	temp = ImageTemplate()
	if tid is None:
		datas = temp.query.all()
		for image_template in datas:
			image_template.content = eval(image_template.content)
	else:
		datas = temp.query.get_or_404(tid)
		datas.content = eval(datas.content)
	return jsonify(datas)


@api.route('/template', methods=['PUT'])
@auth.login_required
def save_template():
	data = request.json
	with db.auto_commit():
		temp = ImageTemplate()
		temp.content = str(data)
		db.session.add(temp)
	return Success()
