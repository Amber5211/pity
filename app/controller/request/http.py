from flask import Blueprint,request
from flask import jsonify
import json

from app.middleware.HttpClient import Request

req=Blueprint('request',__name__,url_prefix='/request')


@req.route('/http',methods=['POST'])
def http_request():
    data=request.get_json()
    method=data.get("method")
    if not method:
        return jsonify(dict(code=101,msg="请求方式不能为空"))

    url=data.get("url")
    if not url:
        return jsonify(dict(code=101,msg="请求地址不能为空"))

    body=json.loads(data.get("body"))

    headers=data.get("headers")
    res=Request(url,json=body,headers=headers)
    response=res.request(method)
    return jsonify(dict(code=0,data=response,msg="操作成功"))