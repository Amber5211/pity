import os

class Config(object):
    ROOT=os.path.dirname(os.path.abspath(__file__))
    LOG_NAME=os.path.join(ROOT,'logs','pity.log')
    JSON_AS_ASCII=False