from flask import Blueprint
from flask import jsonify

auth=Blueprint('auth',__name__,url_prefix='/auth')


@auth.route('/register')
def register():
    return jsonify(status=True,msg='注册成功')
