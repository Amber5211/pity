from flask import Flask
from config import Config

pity = Flask(__name__)
print('================='+__name__)
# 加载配置
pity.config.from_object(Config)