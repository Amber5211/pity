from flask import Flask
from config import Config
from app.controller.auth.user import auth

pity = Flask(__name__)
print('================='+__name__)
# 注册蓝图
pity.register_blueprint(auth)
# 加载配置
pity.config.from_object(Config)