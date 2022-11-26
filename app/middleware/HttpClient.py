import datetime
import requests


class Request(object):
    #初始化方法
    def __init__(self,url,selssion=False,**kwargs):
        '''
        :param url:
        :param selssion: 是否以selssion方式请求
        :param kwargs:
        '''
        self.url=url
        self.selssion=selssion
        self.kwargs=kwargs
        # 判断是否以selssion方式请求
        if self.selssion:
            self.client=requests.session()
            return
        self.client=requests


    @staticmethod
    def get_elapsed(timer:  datetime.timedelta):
        if timer.seconds>0:
            return f"{timer.seconds}.{timer.microseconds//1000}s" # //  表示整数除法,返回不大于结果的一个最大的整数

        return f"{timer.microseconds//100}ms"

    #请求主方法
    def request(self,method:str):
        '''
        :param method: 请求的方式
        :return:
        '''
        status_code = 0
        elapsed = "-1ms"

        try:
            # 根据method调用对应的请求方式
            if method.upper()=='GET': #upper()方法小写字母转化为大写字母
                response=self.client.get(self.url,**self.kwargs)
            elif method.upper()=='POST':
                response=self.client.post(self.url,**self.kwargs)
            else:
                response=self.client.request(method,self.url,**self.kwargs)
            # 获取响应码
            status_code=response.status_code
            # 状态码非200调用Request.response方法status为False
            if status_code !=200:
                return Request.response(False,status_code)
            # 获取响应时间
            elapsed=Request.get_elapsed(response.elapsed)
            # 获取响应体
            data=self.get_response(response)
            # 状态码为200调用Request.response方法status为True
            return Request.response(True,200,data,response.headers,response.request.headers,elapsed=elapsed)

        except Exception as e:
            # 报错调用Request.response方法返回报错信息
            return Request.response(False,status_code,msg=str(e),elapsed=elapsed)



    # get请求方法
    def get(self):
        return self.request('GET')

    # post请求方法
    def post(self):
        return self.request("POST")

    # 根据response返回的类型，返回对应的格式的数据
    def get_response(self,response):
        try:
            return response.json

        except:
            return response.text

    @staticmethod
    def response(status,status_code=200,response=None,response_headers=None,
                 request_headers=None,elapsed=None,msg='success'):
        '''
        :param status: 状态Ture或False
        :param status_code: 响应码，默认为200
        :param response: 响应的内容
        :param response_headers:响应的请求头
        :param request_headers: 请求的请求头
        :param elapsed: 响应时间
        :param msg: 返回的信息，默认为success
        :return:
        '''
        if response_headers is not None:
            response_headers={k: v for k,v in response_headers.items()}
        if request_headers is not None:
            request_headers={k: v for k,v in request_headers.items()}

        return {
            "status":status,
            "status_code":status_code,
            "response":response,
            "response_headers":response_headers,
            "request_headers":request_headers,
            "elapsed":elapsed,
            "msg":msg
        }
