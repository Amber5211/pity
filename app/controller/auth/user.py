from flask import Blueprint,request
from flask import jsonify
from app.controller.auth.UserDao import UserDao
from app.handler.factory import ResponseFactory
from app.middleware.Jwt import UserToken

auth=Blueprint('auth',__name__,url_prefix='/auth')


# 注册用户
@auth.route('/register',methods=['POST'])
def register():
    # 获取请求数据
    data=request.get_json()
    # 获取用户名和密码并判断是否为空
    username,password=data.get('username'),data.get('password')
    if not username or not password:
        return jsonify((dict(code=101,msg='用户名或密码不能为空')))
    # 获取姓名和邮箱并判断是否为空
    email, name = data.get('email'), data.get('name')
    if not email or not name:
        return jsonify((dict(code=101, msg='姓名或邮箱不能为空')))
    # 调用UserDao.register_user方法
    err=UserDao.register_user(username,name,password,email)
    if err is not None:
        return jsonify(dict(code=110,msg=err))

    return jsonify(dict(code=0,msg='注册成功'))

# 登录
@auth.route('/login',methods=['POST'])
def login():
    data=request.get_json()
    username,password=data.get('username'),data.get('password')
    if not username or not password:
        return jsonify(dict(code=101,msg='用户名或密码不存在'))
    user,err=UserDao.login(username,password)
    if err is not None:
        return jsonify(dict(code=110,msg=err))
    # usermodel对象转换成dict
    user=ResponseFactory.model_to_dict(user,'password')
    # 获取token
    token=UserToken.get_token(user)

    return jsonify(dict(code=0,msg='登录成功',data=dict(token=token,user=user)))
    