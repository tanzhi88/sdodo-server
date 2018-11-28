# 权限基类
class Scope:
    allow_api = []
    allow_module = []
    forbidden = []
    # 类中增加有__add__ 方法，则可以使用 + 号进行相加（运算符重载）
    def __add__(self, c):
        self.allow_api += c.allow_api
        # set()使列表变集合，从而去除重复项
        self.allow_api = list(set(self.allow_api))

        # 模块
        self.allow_module += c.allow_module
        self.allow_module = list(set(self.allow_module))
        return self

# 普通用户权限
class UserScope(Scope):
    allow_api = [
        'v1.user+get_user',                 # 获取用户信息(仅自已)
        'v1.user+update_user',              # 更新用户信息(仅自已)
        'v1.coupon+get_coupon_by_tb',   # 从淘宝获取优惠券信息
        'v1.coupon+get_item_by_tb'      # 淘宝客商品查询
    ]
    allow_module = ['v1.quality']

# 管理员权限
class AdminScope(Scope):
    allow_api = []
    allow_module = ['v1.user', 'v1.users']

    def __init__(self):
        self + UserScope()

# 超级管理员
class SuperScope(Scope):
    allow_module = ['v1.task']

    def __init__(self):
        self + UserScope() + AdminScope()


# 验证权限可以访问的接口
def is_in_scope(scope, endpoint):
    # 如果是超级管理员直接跳过
    if scope == 'SuperScope':
        return True
    # 此时传过来的scope是一个字符串，无法直接用scope()来实例一个类
    # Flask 提供一个函数 globals() ,用来将一个模块下所有的变量及类序列化，因此可以用 globals()[scope]的方式
    # 调用scope相应的类
    o = globals()[scope]()
    split = endpoint.split('+')
    red_name = split[0]
    # 按排除
    if endpoint in o.forbidden:
        return False
    # 按视图函数来查看权限
    if endpoint in o.allow_api:
        return True
    # 按模块来查看权限
    if red_name in o.allow_module:
        return True
    else:
        return False