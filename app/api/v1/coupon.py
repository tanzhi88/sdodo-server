from flask import jsonify, request

from app.libs.cache import Cache
from app.libs.redprint import Redprint
from app.libs.spider import Spider
from app.libs.token_auth import auth
from app.models.coupon import Coupon

api = Redprint('coupon')

# 从淘宝获取优惠劵列表
@api.route('')
@auth.login_required
def get_coupon_by_tb():
    param = request.args
    key = param['key'] if 'key' in param else ''
    page = int(param['page']) if 'page' in param else 1
    size = int(param['size']) if 'size' in param else 10
    cache = Cache()
    coupon = cache.get(key=key, page=page, size=size)
    return jsonify(coupon)

# 淘宝客商品查询
@api.route('/search')
@auth.login_required
def get_item_by_tb():

    param = request.json
    spider = Spider()
    return spider.get_coupon_by_cache()
    # coupon = spider.getTbkItem(q=param['q'], cat=param['cat'])
    # return jsonify(coupon)
