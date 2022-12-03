from sqlalchemy import or_
from datetime import datetime

from app.utils.logger import Log
from app.middleware.Jwt import UserToken
from app.models import db
from app.models.user import User


class UserDao(object):
    log=Log('UserDao')

    # 用户注册
    @staticmethod
    def register_user(username,name,password,email):
        '''
        :param username: 用户名
        :param name: 姓名
        :param password: 密码
        :param email: 邮箱
        :return:
        '''
        try:
            users=User.query.filter(or_(User.username==username,User.email==email)).all()
            if users:
                raise Exception('用户名或邮箱已存在')

            # 密码加密
            pwd=UserToken.add_salt(password)
            # 插入user
            user=User(username,name,pwd,email)
            db.session.add(user)
            db.session.commit()

        except Exception as e:
            UserDao.log.error(f'用户注册失败:{str(e)}')
            return str(e)

        return None

    # 登录
    @staticmethod
    def login(username,password):
        '''
        :param username: 用户名
        :param password: 密码
        :return:
        '''
        try:
            # 密码加密
            pwd=UserToken.add_salt(password)
            # 查询用户
            user=User.query.filter_by(username=username,password=pwd,deleted_at=None).first()
            # 判断是否查询到用户
            if user is None:
                return None,'用户名或密码错误'
            # 更新用户最后登录时间
            user.last_login_at=datetime.now()
            db.session.commit()
            return user,None

        except Exception as e:
            UserDao.log.error(f'用户登录失败:{str(e)}')
            return None,str(e)