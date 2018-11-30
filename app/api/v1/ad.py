import os

from flask import current_app

from app.libs.ci import CreatedImage
from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth

api = Redprint('ad')


@api.route('')
@auth.login_required
def create_ad():
	static_path = current_app.config['STATIC_PATH']
	file = static_path + "img/1.jpg"
	items = [
		{
			"type": "img",
			"url": static_path + "/template/base.jpg",
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
	ci = CreatedImage(save_path=file, items=items, size=(400, 710))
	ci.draw()
	ci.save()
	print(s)
	# ci.show()
	return Success()
