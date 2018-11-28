SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:123456@localhost/sdodo'

# 以前默认是True的，版本更新后默认是None了
# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
# 这需要额外的内存， 如果不必要的可以禁用它
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'you-will-never-guess------------------'

TAOBAO_APPKEY = '25229033'
TAOBAO_SECRET = '9cac046902d1ebb89a198f2d1b86f08b'
TAOBAO_ADZONE_ID = 48872350070