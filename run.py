from app import pity

@pity.route('/')

def hello_world():
    print(pity.config.get('ROOT'))
    print(pity.config.get('LOG_NAME'))
    return 'hello world!'


if __name__ == '__main__':
    pity.run("0.0.0.0", threaded=True, port="7777")
    print(pity.url_map)