from app import pity
from app.utils.logger import Log
from app.controller.auth.user import auth

# 注册蓝图
pity.register_blueprint(auth)



@pity.route('/')
def hello_world():
    print(pity.config.get('ROOT'))
    print(pity.config.get('LOG_NAME'))
    log=Log("hello world专用")
    log.info('有人访问你的网站了')
    return 'hello world!'


if __name__ == '__main__':
    print(pity.url_map)
    pity.run("0.0.0.0", threaded=True, port="7777")