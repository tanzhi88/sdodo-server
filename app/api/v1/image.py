from flask import current_app, request, jsonify
from sqlalchemy.testing import in_

from app.libs.ci import CreatedImage
from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.coupon import Coupon

api = Redprint('image')


@api.route('', methods=['PUT'])
@auth.login_required
def created_image():
    data = request.json
    coupon = Coupon.query.filter_by(id=data['coupon_id']).first_or_404()
    static_path = current_app.config['STATIC_PATH']
    template_path = static_path + 'template/'
    save_path = static_path + 'img/'
    ci = CreatedImage(coupon, data['url'], template_path, save_path)
    ci.save()
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
