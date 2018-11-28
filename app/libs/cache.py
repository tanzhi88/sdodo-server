import math
import time

from redis import StrictRedis
from app.libs.mytime import toNumTime


class Cache:

    def __init__(self, host='localhost', port=6379, db=0):
        self.r = StrictRedis(host, port, db, decode_responses=True)
        self.key_table_name = 'key'
        self.value_table_name = 'value'
        self.expired_table_name = 'expired'
        self.test_name = 'test'

    def set_test(self):
        data = time.time()
        self.r.lpush(self.test_name, round(data))
        return data

    # 将数据保存入缓存
    def set(self, data):
        key, value, expired = self._trim_data(data)
        set_key = self._save_key(expired)
        set_value = self._save_value(value)
        if set_key and set_value:
            return True
        else:
            return False

    def get(self, key=None, size=10, page=1):
        ''' 查找相应的缓存 '''
        if key:
            return eval(self.r.hget(self.value_table_name, key))

        # 查找总的计录条数
        total = self.r.zcard(self.key_table_name)
        # 计算总页数
        total_page = math.ceil(total / size)
        if page > total_page:
            page = total_page
        # 计算开始位置
        s = (page - 1) * size
        e = s + size -1
        key = self.r.zrange(self.key_table_name, s, e)
        sset = self.r.hmget(self.value_table_name, key)
        values = []
        for value in sset:
            values.append(eval(value))
        return {'coupons':values, 'current_page':page, 'page_size':size, 'total':total, 'total_page':total_page}

    def _trim_data(self, datas):
        '''整理数据，使之能正确写入缓存'''

        # 先将数据整理成三份
        key = []
        value = {}
        expired = []
        for data in datas:
            if data['num_iid'] and data['coupon_end_time']:
                id = data['num_iid']
                # 数据的键值，存入list中，用来做分页
                key.append(id)
                # 数据的过期时间，存入list中
                tnum = round(toNumTime(data['coupon_end_time']))
                t = {'id': id, 'expired': tnum}
                expired.append(t)
                # 数据值，存入str中
                value[id] = str(data)
        return key,value,expired

    def _save_value(self, value):
        ''' 对数据值进行保存 '''
        return self.r.hmset(self.value_table_name, value)

    def _save_key(self, keys):
        ''' 对键值进行保存 '''
        for key in keys:
            self.r.zadd(self.key_table_name, {key['id']:key['expired']})
        return True

    # 删除已经过期的缓存
    def _del_expired(self):
        pass



if __name__ == '__main__' :
    cache = Cache()
    data = [
    {
        "category": 50008165,
        "commission_rate": "1.50",
        "coupon_click_url": "https://uland.taobao.com/coupon/edetail?e=pGC7YqxhjhMGQASttHIRqQlQHzu42%2BVfapwq%2FsgvctRUm%2Fg8xRLmNoH5CBwYWiPlGNAXFw9kHeRO44hx%2Bv3Av9k%2FK2ALhul5bd76m3V5xpZ%2BeoXZPWxxAUZQaMuKxqbZwd6gSKhGMg%2FiBa27Bqy4sbGk2dypsnoweeWR4cNxntz7J8FmRkgg%2BNboO99VQREJtJtwpJuhjdim5%2Bfl6RVop2WkWFLiP7OTHL46ZcydpNI%3D&traceId=0b175b5415422427669296904e",
        "coupon_end_time": "2018-11-17",
        "coupon_info": "满6元减1元",
        "coupon_remain_count": 8292,
        "coupon_start_time": "2018-11-13",
        "coupon_total_count": 10000,
        "item_description": "",
        "item_url": "https://detail.tmall.com/item.htm?id=574357840297",
        "nick": "倾情一笑",
        "num_iid": 574357840297,
        "pict_url": "http://img.alicdn.com/tfscom/i5/804464091/tb-831795275.jpg+%23/TB2jCIOd9OI.eBjSspmXXatOVXa%5f%21!2088419953.jpg",
        "seller_id": 3890490369,
        "shop_title": "恒源顺家居企业店",
        "small_images": {
            "string": [
                "http://img.alicdn.com/tfscom/i5/737478316/tb-327704477.jpg+%23/TB2CZQudY5K.eBjy0FfXXbApVXa%5f%21!2088419953.jpg",
                "http://img.alicdn.com/tfscom/i5/716382985/tb-477472860.jpg+%23/TB1D9yJNXXXXXb9apXXYXGcGpXX%5fM2.SS2",
                "http://img.alicdn.com/tfscom/i5/237746510/tb-824557513.jpg+%23/TB1oHOEJXXXXXbmXVXXYXGcGpXX%5fM2.SS2",
                "http://img.alicdn.com/tfscom/i5/457772955/tb-310957791.jpg+%23/TB2v6%5fthbsTMeJjSszdXXcEupXa%5f%21!2088419953.jpg"
            ]
        },
        "title": "新款条绒宝宝防尿裤裤儿童尿不湿皮裤婴儿防水罩裤宝宝隔尿裤",
        "user_type": 0,
        "volume": 3,
        "zk_final_price": "6.55"
    },
    {
        "category": 16,
        "commission_rate": "9.00",
        "coupon_click_url": "https://uland.taobao.com/coupon/edetail?e=UXOqTp1ZdB4GQASttHIRqTP5P8mkQy0OK9BUWDTTgaoh4%2FBFCEkLWHMY63BtDxC5eLzfTaq6Pjlku97ifcjBZWsYiQRkxJlibd76m3V5xpZ%2BeoXZPWxxAUZQaMuKxqbZwd6gSKhGMg%2FiBa27Bqy4sbGk2dypsnoweeWR4cNxntzk92%2BM7h46c9boO99VQREJuFuGhSUVywwfi2iNaylAvdjH%2B8knoxVQZAipt4EQy3w%3D&traceId=0b175b5415422427669296904e",
        "coupon_end_time": "2018-11-14",
        "coupon_info": "满15元减10元",
        "coupon_remain_count": 1,
        "coupon_start_time": "2018-11-14",
        "coupon_total_count": 10,
        "item_description": "",
        "item_url": "https://detail.tmall.com/item.htm?id=580181306697",
        "nick": "偶遇幸福时光",
        "num_iid": 580181306697,
        "pict_url": "http://img.alicdn.com/tfscom/i2/1806393463/O1CN011bS62jptqQJlChp_!!1806393463.jpg",
        "seller_id": 1806393463,
        "shop_title": "Oni Girls 软糯少女韩系定制",
        "small_images": {
            "string": [
                "http://img.alicdn.com/tfscom/i2/1806393463/O1CN011bS62nL62wYbf3A_!!1806393463.jpg",
                "http://img.alicdn.com/tfscom/i3/1806393463/O1CN011bS62m9jaLUrbW0_!!1806393463.jpg",
                "http://img.alicdn.com/tfscom/i2/1806393463/O1CN011bS62ltqXbG26oA_!!1806393463.jpg",
                "http://img.alicdn.com/tfscom/i1/1806393463/O1CN011bS62mk1Hzcrcsf_!!1806393463.jpg"
            ]
        },
        "title": "韩国ins 鬼马软糯少女可爱减龄毛茸茸卫衣+灯芯绒背带连体裤套装",
        "user_type": 0,
        "volume": 47,
        "zk_final_price": "53.00"
    },
    {
        "category": 16,
        "commission_rate": "4.50",
        "coupon_click_url": "https://uland.taobao.com/coupon/edetail?e=HLTflVtucmoGQASttHIRqaP6aN2GPaU32Fv5JS6RxKHyi1aSyqbpmibEnvUHWoKibkl6ti2XGAX16oDV%2BkCgTZwkYAQ1r9IAbd76m3V5xpZ%2BeoXZPWxxAUZQaMuKxqbZwd6gSKhGMg%2FiBa27Bqy4sbGk2dypsnoweeWR4cNxntzk92%2BM7h46c9boO99VQREJuFuGhSUVywwfi2iNaylAvdjH%2B8knoxVQZAipt4EQy3w%3D&traceId=0b175b5415422427669296904e",
        "coupon_end_time": "2018-11-30",
        "coupon_info": "满1元减1元",
        "coupon_remain_count": 71000,
        "coupon_start_time": "2018-11-13",
        "coupon_total_count": 100000,
        "item_description": "",
        "item_url": "https://detail.tmall.com/item.htm?id=578063007801",
        "nick": "tb154106_33",
        "num_iid": 578063007801,
        "pict_url": "http://img.alicdn.com/tfscom/i3/898039156/O1CN012HVUpzYQO9lddhi_!!898039156.jpg",
        "seller_id": 898039156,
        "shop_title": "港岛家居旗 舰 店",
        "small_images": {
            "string": [
                "http://img.alicdn.com/tfscom/i1/898039156/O1CN012HVUq1O9Gx7AQHz_!!898039156.jpg",
                "http://img.alicdn.com/tfscom/i2/898039156/O1CN012HVUpzYQrFtvjDI_!!898039156.jpg",
                "http://img.alicdn.com/tfscom/i2/898039156/O1CN012HVUq24SQirIZWY_!!898039156.jpg",
                "http://img.alicdn.com/tfscom/i2/898039156/O1CN012HVUpzYR3jQDxuU_!!898039156.jpg"
            ]
        },
        "title": "秋季新款复古风修身显瘦前后两穿打底长袖T恤+高腰百褶银色阔腿裤",
        "user_type": 0,
        "volume": 0,
        "zk_final_price": "3.29"
    }
    ]
    # cache.r.zadd('zz' 'n1', 1)
    d = cache.set(data)
    # d = cache.get()
    # d1 = dict(d[0])
    # d1 = eval(d[0])
    # print(type(d))
    # t = toNumTime("2018-11-17")
    print(d)
    # values,total_page,page = cache.get()
    # print(values[0]['category'])

    # json_data = json.dumps(data)
    # o_data = json.loads(json_data)
    # print(type(json_data), type(o_data))
    # print(o_data[0]['category'])

    # page = 1
    # size = 2
    # total = 7
    # s = (page-1) * size
    # s = 0
    # e = 0 + 2
    # l = [1,3,4,5,6,7,8]
    # l1 = l[0:2]
    # print(l1)