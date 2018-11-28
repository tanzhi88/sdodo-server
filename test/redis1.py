import json

from flask import jsonify
from redis import StrictRedis

r = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
# r.zadd('znum', 1,2)


data = {
    'category': 50008165,
    'commission_rate': '1.50',
    'coupon_click_url': 'https://uland.taobao.com/coupon/edetail?e=pGC7YqxhjhMGQASttHIRqQlQHzu42%2BVfapwq%2FsgvctRUm%2Fg8xRLmNoH5CBwYWiPlGNAXFw9kHeRO44hx%2Bv3Av9k%2FK2ALhul5bd76m3V5xpZ%2BeoXZPWxxAUZQaMuKxqbZwd6gSKhGMg%2FiBa27Bqy4sbGk2dypsnoweeWR4cNxntz7J8FmRkgg%2BNboO99VQREJtJtwpJuhjdim5%2Bfl6RVop2WkWFLiP7OTHL46ZcydpNI%3D&traceId=0b175b5415422427669296904e',
    'coupon_end_time': '2018-11-17',
    'coupon_info': '满6元减1元',
    'coupon_remain_count': 8292,
    'coupon_start_time': '2018-11-13',
    'coupon_total_count': 10000,
    'item_description': '',
    'item_url': 'https://detail.tmall.com/item.htm?id=574357840297',
    'nick': '倾情一笑',
    'num_iid': 574357840297,
    'pict_url': 'http://img.alicdn.com/tfscom/i5/804464091/tb-831795275.jpg+%23/TB2jCIOd9OI.eBjSspmXXatOVXa%5f%21!2088419953.jpg',
    'seller_id': 3890490369,
    'shop_title': '恒源顺家居企业店',
    'small_images':
        {
            'string': [
                'http://img.alicdn.com/tfscom/i5/737478316/tb-327704477.jpg+%23/TB2CZQudY5K.eBjy0FfXXbApVXa%5f%21!2088419953.jpg',
                'http://img.alicdn.com/tfscom/i5/716382985/tb-477472860.jpg+%23/TB1D9yJNXXXXXb9apXXYXGcGpXX%5fM2.SS2',
                'http://img.alicdn.com/tfscom/i5/237746510/tb-824557513.jpg+%23/TB1oHOEJXXXXXbmXVXXYXGcGpXX%5fM2.SS2',
                'http://img.alicdn.com/tfscom/i5/457772955/tb-310957791.jpg+%23/TB2v6%5fthbsTMeJjSszdXXcEupXa%5f%21!2088419953.jpg'
            ]
        },
    'title': '新款条绒宝宝防尿裤裤儿童尿不湿皮裤婴儿防水罩裤宝宝隔尿裤',
    'user_type': 0,
    'volume': 3,
    'zk_final_price': '6.55'
}
print(type(data))
# print(str(data))
# a = r.hmset('aa',{'aa':str(data)})
# a = r.hmget('value',[574357840297,580181306697,578063007801])
# a = r.sadd('sex','11')
a = r.zadd('myset',{123:456})
# a = r.zrange('myset',0,-1)
# print(type(a))
# print(jsonify(a))
print(a)