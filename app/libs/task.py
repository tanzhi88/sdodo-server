# from apscheduler.schedulers.background import BackgroundScheduler
import time

from apscheduler.schedulers.blocking import BlockingScheduler

from app.libs.spider import Spider
from app.config.secure import TAOBAO_APPKEY, TAOBAO_SECRET, TAOBAO_ADZONE_ID

scheduler = BlockingScheduler()
# schedulers = BackgroundScheduler()


class Task:
    '''
    采集任务
    '''

    def __init__(self, q=None, page=10, size=10):
        self.page = page
        self.size = size
        self.q = q
        self.current_page = 1

    def go(self):
        result = {}
        while (self.current_page <= self.page) & (result is not None):
            result = self.do()
            self.current_page += 1
            # time.sleep(2)
        return True

    def do(self):
        # q = '美特斯邦威旗舰店正品官方女装2018春装新款棉服夹克女韩版休闲短'
        spider = Spider()
        coupons = spider.get_tbk_coupon(q=self.q, size=self.size, page=self.current_page)
        return coupons


if __name__ == '__main__':

    task = Task()
    c = task.do()
    print(c)
