from flask import Blueprint,request
from flask import jsonify
import json

from app.middleware.HttpClient import Request
from app.utils.decorator import permission

req=Blueprint('request',__name__,url_prefix='/request')


@req.route('/http',methods=['POST'])
@permission()
def http_request(user_info):
    data=request.get_json()
    method=data.get("method")
    if not method:
        return jsonify(dict(code=101,msg="请求方式不能为空"))

    url=data.get("url")
    if not url:
        return jsonify(dict(code=101,msg="请求地址不能为空"))

    if data.get("body")==None:
        body=data.get("body")
    else:
        body=json.loads(data.get("body"))

    headers=data.get("headers")
    res=Request(url,json=body,headers=headers)
    response=res.request(method)
    if response.get('status'):
        return jsonify(dict(code=0,data=response,msg="操作成功"))
    return jsonify(dict(code=110,data=response,msg=response.get('msg')))