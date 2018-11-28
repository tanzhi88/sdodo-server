'''
世界上有两种标准时间的格式 一种是UTC 标准时区，另一种的夏令时的标准时区。中国使用的是UTC+8的一个时间 。就是北京时间
时间分为 三种格式
1. struct_time格式（就是tuple 元组的一种时间格式)
>>> time.localtime()
time.struct_time(tm_year=2018, tm_mon=2, tm_mday=3, tm_hour=14, tm_min=54, tm_se
c=50, tm_wday=5, tm_yday=34, tm_isdst=0)

2. 时间戳
>>> time.time()
1517640828.0257125

3. 格式化的时间格式
例如：2018-02-03 14-36-01

三个格式间的相互转换
格式化的时间想转成时间戳，必须先将格式化时间转成 struct_time 的格式, 再将 struct_time 的格式转时间戳
1、 str_time = '2018-11-01 0:0:0'
2、 uct_time = time.strptime(str_time,"%Y-%m-%d %H:%M:%S")
3、 int_time = time.mktime(uct_time)
时间戳格式转回格式化时间，必须先将时间戳转成 struct_time 的格式, 再将 struct_time 的格式转格式化时间
1、 int_time2 = 1541001600
2、 uct_time2 = time.localtime(int_time2)
3、 str_time2 = time.strftime("%Y-%m-%d %H:%M:%S", uct_time2)
'''

# 时间戳转格式化时间
import time


def toStrTime(num_time=0, format_str = "%Y-%m-%d"):
	if not num_time:
		num_time = time.time()
	return time.strftime(format_str, time.localtime(num_time))

# 格式化时间转时间戳
def toNumTime(str_time, format_str = "%Y-%m-%d"):
	return time.mktime(time.strptime(str_time, format_str))