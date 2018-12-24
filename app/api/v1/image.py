from flask import current_app, request

from app.libs.ci import CreatedImage
from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.coupon import Coupon

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
