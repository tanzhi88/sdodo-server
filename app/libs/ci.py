import io
import qrcode
from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen


class CreatedImage(object):
    """生成图片"""

    def __init__(self, coupon, url, template_path, save_path):
        self.font_f = template_path + 'simhei.TTF'
        # 主图
        self.main = Image.open(template_path + 'base.jpg')
        # id
        # self.coupon_id = coupon['id']
        self.coupon_id = coupon.id
        # 产品图
        self.img1 = coupon.pict_url.url
        self.img2 = coupon.small_pic[0].url
        self.img3 = coupon.small_pic[1].url
        self.img4 = coupon.small_pic[2].url
        # 二维码地址
        self.url = url + str(self.coupon_id)
        # 原价
        self.yj = coupon.zk_final_price
        # 优惠劵面额
        self.me = coupon.coupon_price
        # 劵后价
        self.jh = round(self.yj - self.me, 2)
        # 标题
        self.title = coupon.title
        # 左边绘制的X坐标
        self.x = 10
        # 保存路径
        self.save_path = save_path + str(self.coupon_id) + '.png'

        self.go()

    # 获取标题
    def getTitles(self):
        titles = []
        # 先获取总长
        t_len = len(self.title)
        # 每次被截取后的长度
        s_len = t_len
        # 每次截取的固定长度
        g_len = 15
        # 循环获取每段固定文字,如果被截取后的长度比固定长度大则继续
        while s_len > 0:
            # 计算本次要从哪开始，哪结束
            s = t_len - s_len
            e = s + g_len
            s_len -= g_len
            titles.append(self.title[s:e])
        return titles

    # 绘制标题
    def drawTitle(self):
        draw = ImageDraw.Draw(self.main)
        ft = ImageFont.truetype(self.font_f, 16)
        h = 20  # 行高
        y = 560  # 首行y坐标
        titles = self.getTitles()
        for title in titles:
            draw.text((self.x, y), title, (51, 51, 51), font=ft)
            y += h

    # 绘制文字
    def drawText(self, zb, c, size=16, color=(153, 153, 153)):
        draw = ImageDraw.Draw(self.main)
        ft = ImageFont.truetype(self.font_f, size)
        draw.text(zb, c, color, font=ft)

    # 粘贴图片
    # box 为要粘贴的位置， url为图片的网络地址
    def pasteImg(self, url, box):
        img = Image.open(self.getImgByUrl(url))
        # 要将图片缩放成与粘贴位置大小相同，否则报错，Image.ANTIALIAS 为滤镜，缩小后不模糊
        img = img.resize((box[2] - box[0], box[3] - box[1]), Image.ANTIALIAS)
        self.main.paste(img, box)

    # 获取网络图片
    def getImgByUrl(self, url):
        image_bytes = urlopen(url).read()
        data_stream = io.BytesIO(image_bytes)
        return data_stream

    # 贴二维码
    def pasteQr(self):
        box = (264, 555, 389, 679)
        img = qrcode.make(self.url)
        img = img.resize((box[2] - box[0], box[3] - box[1]), Image.ANTIALIAS)
        self.main.paste(img, box)

    # 主操作
    def go(self):
        # 贴主图
        self.pasteImg(self.img1, (10, 25, 390, 410))
        # 贴小图
        self.pasteImg(self.img2, (10, 415, 135, 540))
        self.pasteImg(self.img3, (137, 415, 262, 540))
        self.pasteImg(self.img4, (265, 415, 390, 540))
        # 贴二维码
        self.pasteQr()
        # 写标题
        self.drawTitle()
        # 写原价
        self.drawText((50, 632), str(self.yj) + "元")
        # 写面额
        self.drawText((32, 662), str(self.me) + "元", 14, (255, 65, 31))
        # 写卷后
        self.drawText((134, 656), str(self.jh) + "元", 24, (255, 65, 31))

    # 保存

    def save(self):
        self.main.save(self.save_path)

    # 显示图片
    def show(self):
        self.main.show()


if __name__ == '__main__':
    coupon = {
        'id': 1,
        'title': '香蕉芭那那 秋冬学院风格子长袖衬衫+拼色v领马甲+铅笔裤三件套女',
        'bimg': 'http://img.alicdn.com/tfscom/i1/605781181/TB1LCwDn8jTBKNjSZFuXXb0HFXa_!!0-item_pic.jpg',
        'simg': [
            'http://img.alicdn.com/tfscom/i3/1939576703/TB267ZjotcnBKNjSZR0XXcFqFXa_!!1939576703.jpg',
            'http://img.alicdn.com/tfscom/i1/1939576703/TB2nunLoOMnBKNjSZFCXXX0KFXa_!!1939576703.jpg',
            'http://img.alicdn.com/tfscom/i3/1939576703/TB2C0hRoAUmBKNjSZFOXXab2XXa_!!1939576703.jpg'],
        'zk_final_price': 89.9,
        'coupon_price': 50}

    coupon = {
        'id': 2,
        'category': 50008090,
        'commission_rate': '5.85',
        'coupon_click_url': 'https://uland.taobao.com/coupon/edetail?e=2JLyr%2FUTspwGQASttHIRqQeRhjsHiNBx3qfmEVXmOdfyi1aSyqbpmlcSJt%2BtWAWIBGGYNpl%2BSdEv5Ta5P2EUeXbLUECVZbOXbd76m3V5xpZ%2BeoXZPWxxAUZQaMuKxqbZwd6gSKhGMg%2FiBa27Bqy4sbGk2dypsnoweeWR4cNxntzk92%2BM7h46c9boO99VQREJuFuGhSUVywwfi2iNaylAvdjH%2B8knoxVQ4V7BXID%2Bxs8%3D&traceId=0b1748fe15432199544414475e',
        'coupon_end_time': '2018-11-26',
        'coupon_info': '满5元减3元',
        'coupon_remain_count': 43,
        'coupon_start_time': '2018-11-26',
        'coupon_total_count': 60,
        'item_description': '',
        'item_url': 'https://detail.tmall.com/item.htm?id=581185577265',
        'nick': '小妖精560203',
        'num_iid': 581185577265,
        'pict_url': 'http://img.alicdn.com/tfscom/i2/3403999587/O1CN015NeaPb2KgtYSrMaWQ_!!3403999587.jpg',
        'seller_id': 3403999587,
        'shop_title': '小妖精杂货铺123',
        'small_pic': {
                'http://img.alicdn.com/tfscom/i2/3403999587/O1CN012KgtYSKvZVo2wvM_!!3403999587.jpg',
                'http://img.alicdn.com/tfscom/i2/3403999587/O1CN012KgtYSKxW4E22Dy_!!3403999587.jpg',
                'http://img.alicdn.com/tfscom/i1/3403999587/O1CN01ky9n5c2KgtYTU6CRQ_!!3403999587.jpg'},
        'title': '华为nova青春版手机软壳5.2WAS一al00钢化膜一体女tl10支架aloo潮',
        'user_type': 0,
        'volume': 0,
        'zk_final_price': '28.00',
        'coupon_price': 3,
        'token': '￥h9J0bP5Aiop￥'}
    # print(coupon['bimg'])
    # ci = CreatedImage(coupon, 'http://sdodo.read80.cn/s/')
    # ci.save()

    import os

    basedir = os.path.abspath(os.path.dirname(__file__))
    dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    static_path = dir + r'\/static\/template\/'
    save_path = dir + r'\/static\/img\/'

    ci = CreatedImage(
        coupon,
        'http://sdodo.read80.cn/s/',
        static_path,
        save_path)
    # ci.show()
    ci.save()
