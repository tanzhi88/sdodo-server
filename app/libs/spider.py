import re

from flask import current_app, jsonify
from app import create_app

import top
import time

from app.libs.cache import Cache
from app.libs.error_code import ServerError


class Spider:
    def __init__(self):
        self.appkey = current_app.config['TAOBAO_APPKEY']
        self.secret = current_app.config['TAOBAO_SECRET']
        self.adzone_id = int(current_app.config['TAOBAO_ADZONE_ID'])
        self.app_info = top.appinfo(self.appkey, self.secret)
        self.cache = Cache()

    # 从缓存中获取
    def get_coupon_by_cache(self, key=None, size=10, page=1):
        return self.cache.get(key, size, page)

    # 循环写入缓存
    def save_cache(self, datas):
        return self.cache.set(datas)

    # 从好券清单获取优惠卷
    def get_tbk_coupon(self, q='', size=100, page=1):

        req = top.api.TbkDgItemCouponGetRequest()
        req.set_app_info(self.app_info)

        req.adzone_id = self.adzone_id
        req.platform = 2
        req.page_size = size
        req.page_no = page
        req.q = q
        try:
            r = req.getResponse()
            resp = r['tbk_dg_item_coupon_get_response']['results']['tbk_coupon']
            result = self.set_token(resp)
            if self.save_cache(result):
                return result
            return None
        except Exception as e:
            print('err:', e)
            return None

    # 获取优惠券信息
    def get_coupon_info(self, me):
        req = top.api.TbkCouponGetRequest()
        req.set_app_info(self.app_info)

        req.me = me
        # req.item_id = 123
        # req.activity_id = "sdfwe3eefsdf"
        try:
            resp = req.getResponse()
            return jsonify(resp)
        except Exception as e:
            raise ServerError()

    # 循环获取淘口令
    def set_token(self, coupons):
        for item in coupons:
            # 通过正则表达式提取优惠券信息中的面额
            item['coupon_price'] = int(re.findall(r'(\d+)', item['coupon_info'])[-1])
            # 获取淘口令
            item['token'] = self.get_coupon_token(url=item['coupon_click_url'], text=item['title'])
        return coupons

    # 获取淘口令

    def get_coupon_token(self, url, text):
        req = top.api.TbkTpwdCreateRequest()
        req.set_app_info(self.app_info)

        req.text = text
        req.url = url
        try:
            resp = req.getResponse()['tbk_tpwd_create_response']['data']['model']
            return resp
        except Exception as e:
            raise ServerError()
        return None

    # 淘宝客商品查询
    def getTbkItem(self, q='', cat=None):
        req = top.api.TbkItemGetRequest()
        req.set_app_info(self.app_info)

        req.fields = 'req.fields="num_iid,title,pict_url,small_images,reserve_price,zk_final_price,user_type,provcity,item_url,seller_id,volume,nick"'
        req.q = q
        # req.cat = cat
        try:
            resp = req.getResponse()
            return resp
        except Exception as e:
            print(e)

    # 获取后台供卖家发布商品的标准商品类目
    def getCat(self):
        req = top.api.ItemcatsGetRequest()
        req.set_app_info(self.app_info)

        # req.cids = "16"
        req.datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        req.fields = "cid,parent_cid,name,is_parent"
        # req.parent_cid = 50011999
        try:
            resp = req.getResponse()
            return resp
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        spider = Spider()
        coupon = spider.get_tbk_coupon()
        print(coupon)
