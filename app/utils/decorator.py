'''
    这是一个装饰器方法文件
'''

from functools import wraps
from flask import request,jsonify
from app import pity
from app.middleware.Jwt import UserToken

FORBIDDEN="对不起，你没有足够的权限"

# 单例类的装饰器
class SingletonDecorator():

    def __init__(self,cls):
        self.cls=cls
        self.instance=None


    def __call__(self, *args, **kwargs):
        # 首先判断该类的实例是否是None，为None的话则生成新实例，否则返回该实例。这样就确保了只生成一次实例。
        if self.instance is None:
            self.instance=self.cls(*args,**kwargs)

        return self.instance


# 自动判断用户token是否有效以及获取用户信息装饰器
def permission(role=pity.config.get("GUEST")):
    def login_required(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            try:
                # 获取请求头
                headers=request.headers
                # 获取token
                token=headers.get('token')
                # token为None，返回信息
                if token is None:
                    return jsonify(dict(code=401,msg='用户信息认证失败，请检查'))
                # 解析token，获取用户信息
                user_info=UserToken.parse_token(token)
                # 把user_info信息写入kwargs
                kwargs['user_info']=user_info
            except Exception as e:
                print(dict(code=401,msg=str(e)))
                return jsonify(dict(code=401,msg=str(e)))
            # 判断用户的权限是否足够，如果不够直接返回对应提示
            if user_info.get('role',0)<role:
                return jsonify(dict(code=400,msg=FORBIDDEN))
            return func(*args,**kwargs)


        return wrapper

    return login_required