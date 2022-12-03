import os

class Config(object):
    ROOT=os.path.dirname(os.path.abspath(__file__))
    LOG_NAME=os.path.join(ROOT,'logs','pity.log')
    # jsonify编码问题
    JSON_AS_ASCII=False

    # mysql数据库连接信息
    MYSQL_HOST='127.0.0.1'
    MYSQL_PORT=3306
    MYSQL_USER='root'
    MYSQL_PWD='123456'
    DBNAME='pity'

    #SQLAlchemy
    SQLALCHEMY_DATABASE_URI=f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/{DBNAME}'

    SQLALCHEMY_TRACK_MODIFICATIONS=False

    # 用户角色配置
    GUEST=0
    ADMIN=2
