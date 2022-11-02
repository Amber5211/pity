import hashlib
from datetime import timedelta,datetime

import jwt
from jwt.exceptions import ExpiredSignatureError

EXPIRED_HOUR =3


class UserToken(object):
    key='pityToken'
    salt='pity'

    # 获取token
    @staticmethod
    def get_token(data):
        new_data=dict({'exp':datetime.utcnow()+timedelta(hours=EXPIRED_HOUR)},**data)

        return jwt.encode(new_data,key=UserToken.key)

    # 解析token
    @staticmethod
    def parse_token(token):
        try:
            return jwt.decode(token,key=UserToken.key)

        except:
            raise Exception("token已过期, 请重新登录")


    #密码md5加密
    @staticmethod
    def add_salt(password):
        '''
        :param password: 密码
        :return:
        '''
        m=hashlib.md5()
        m.update((password+UserToken.salt).encode('utf-8'))

        return m.hexdigest()




