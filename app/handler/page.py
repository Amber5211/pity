'''
获取分页的相关方法
'''

from flask import request

# 默认页数和页码
PAGE=1
SIZE=10

class PageHandler(object):

    @staticmethod
    def page():
        '''
        获取page和size
        :return:
        '''
        page=request.args.get("page")#equest.args.get()获取地址栏中参数
        if page is None or not page.isdigit():#isdigit()方法判断是否为数字
            page=PAGE

        size=request.args.get("size")
        if size is None or not size.isdigit():
            size=SIZE

        return int(page),int(size)