import io
import os

import qrcode
from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen


class CreatedImage:
	"""生成图片"""

	def __init__(self, save_path, items, size=(100, 50), save_format='jpeg', save_quality=60):
		"""
		:param save_path: 需要保存地址
		:param items: 要生成的图片里的各个元素及粘贴位置等信息
		:param size: 生成的图片的大小尺寸
		:param save_format: 保存图片的格式
		:param save_quality: 保存图片的质量
		"""
		base_path = os.path.abspath(os.path.dirname(__file__))
		self.font_f = base_path + '/simhei.TTF'
		self.size = size
		self.save_path = save_path
		self.items = items
		self.image = Image.new("RGB", self.size, (255, 255, 0))
		self.save_format = save_format
		self.save_quality = save_quality

	def _draw_text(self, xy, text, size=16, color=(153, 153, 153)):
		"""
		绘制文字
		:param xy: 文本起始点的坐标
		:param text: 文本内容
		:param size: 文字大小
		:param color: 文字颜色
		"""
		draw = ImageDraw.Draw(self.image)
		# 设置字体
		ft = ImageFont.truetype(self.font_f, size)
		draw.text(xy, text, color, font=ft)

	def _paste_img(self, url, box, local=True, qr=False):
		"""
		粘贴图片
		:param url: 要粘贴的图片地址
		:param box: 要粘贴的位置，此参数为一个有4个元素的元组，分别是左、上、右、下
		:param local: 是否是本地图片
		:param qr: 是否是二维码
		被粘贴的元素必须和box的大小相同
		"""
		# 如果是二维码单独处理
		if qr:
			img = qrcode.make(url, border=1)
		else:
			# 网络图片与本地图片分开处理
			img = Image.open(url) if local else Image.open(self._get_img_by_url(url))
		# 要将图片缩放成与粘贴位置大小相同，否则报错，Image.ANTIALIAS 为滤镜，缩小后不模糊
		img = img.resize((box[2] - box[0], box[3] - box[1]), Image.ANTIALIAS)
		self.image.paste(img, box)

	def draw(self):
		"""
		循环将所有元素进行绘制
		"""
		for item in self.items:
			if item['type'] == 'img':
				qr = True if 'qr' in item else False
				local = True if 'local' in item else False
				self._paste_img(item['url'], item['box'], local, qr)
			elif item['type'] == 'text':
				# 如果设置了文本换行，则先把文本进行整理加入换行符
				text = self._trim_text(item['text'], item['newline']) if 'newline' in item else item['text']
				self._draw_text(item['xy'], text, item['size'], item['color'])

	@staticmethod
	def _get_img_by_url(url):
		"""
		获取网络图片
		:param url: 图片地址，如果是二维码则是二维码的地址
		:return: img 图片对像
		"""
		image_bytes = urlopen(url).read()
		data_stream = io.BytesIO(image_bytes)
		return data_stream

	@staticmethod
	def _trim_text(text, newline):
		"""
		动态的给文本加上换行符
		:param text: 要整理的文本
		:param newline: 设置多少个字符就进行换行
		:return: 加入换行符的文本
		"""
		text_list = []
		# 先获取总长
		t_len = len(text)
		# 每次被截取后的长度
		s_len = t_len
		# 每次截取的固定长度
		g_len = newline
		# 循环获取每段固定文字,如果被截取后的长度比固定长度大则继续
		while s_len > 0:
			# 计算本次要从哪开始，哪结束
			s = t_len - s_len
			e = s + g_len
			s_len -= g_len
			text_list.append(text[s:e])
		return '\n'.join(text_list)

	# 保存
	def save(self):
		self.image.save(self.save_path, format=self.save_format, quality=self.save_quality)

	# 显示图片
	def show(self):
		self.image.show()


if __name__ == '__main__':

	basedir = os.path.abspath(os.path.dirname(__file__))
	dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
	static_path = dir + r'\\app\\static\\template\\'
	path = dir + r'\\app\\static\\img\\1_1.jpg'

	item = [
		{
			"type": "img",
			"url": static_path + "base.jpg",
			"local": True,
			"box": (0, 0, 400, 710)
		},
		{
			"type": "img",
			"url": "http://img.alicdn.com/tfscom/i1/605781181/TB1LCwDn8jTBKNjSZFuXXb0HFXa_!!0-item_pic.jpg",
			"box": (10, 25, 390, 410)
		},
		{
			"type": "img",
			"url": "http://img.alicdn.com/tfscom/i3/1939576703/TB267ZjotcnBKNjSZR0XXcFqFXa_!!1939576703.jpg",
			"box": (10, 415, 135, 540)
		},
		{
			"type": "img",
			"url": "http://img.alicdn.com/tfscom/i1/1939576703/TB2nunLoOMnBKNjSZFCXXX0KFXa_!!1939576703.jpg",
			"box": (137, 415, 262, 540)
		},
		{
			"type": "img",
			"url": "http://img.alicdn.com/tfscom/i3/1939576703/TB2C0hRoAUmBKNjSZFOXXab2XXa_!!1939576703.jpg",
			"box": (265, 415, 390, 540)
		},
		{
			"type": "text",
			"xy": (10, 560),
			"text": "香蕉芭那那 秋冬学院风格子长袖衬衫+拼色v领马甲+铅笔裤三件套女",
			"newline": 15,
			"size": 16,
			"color": (153, 153, 153)
		},
		{
			"type": "text",
			"xy": (50, 632),
			"text": "50元",
			"size": 16,
			"color": (153, 153, 153)
		},
		{
			"type": "text",
			"xy": (32, 662),
			"text": "5元",
			"size": 14,
			"color": (255, 65, 31)
		},
		{
			"type": "text",
			"xy": (134, 656),
			"text": "45元",
			"size": 24,
			"color": (255, 65, 31)
		},
		{
			"type": "img",
			"url": "http://sdodo.read80.cn/s/1",
			"qr": True,
			"box": (264, 555, 389, 679)
		}
	]

	ci = CreatedImage(path, item, (400, 710))
	ci.draw()
	# ci.show()
	ci.save()
