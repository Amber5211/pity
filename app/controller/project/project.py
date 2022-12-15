from flask import Blueprint,request,jsonify

from app import pity
from app.utils.decorator import permission
from app.handler.page import PageHandler
from app.dao.project.ProjectDao import ProjectDao
from app.handler.factory import ResponseFactory



pr=Blueprint('project',__name__,url_prefix='/project')

@pr.route('/list')
@permission()
def list_project(user_info):
    '''
    获取项目列表
    :param user_info:
    :return:
    '''
    # 获取分页
    page,size=PageHandler.page()
    # 获取用户role和user_id
    role=user_info['role']
    user_id=user_info['id']
    # 获取name参数
    name=request.args.get('name')
    # 调用ProjectDao.list_project方法查询用户的项目
    result,total,err=ProjectDao.list_project(user_id,role,page,size,name)

    if err is not None:
        return jsonify(dict(code=110,data=result,msg=err))

    return jsonify(dict(code=0,data=ResponseFactory.model_to_list(result),msg='操作成功'))


@pr.route('/insert',methods=['POST'])
@permission(role=pity.config.get('MANAGER'))
def insert_project(user_info):
    '''
    新增项目
    :param user_info:
    :return:
    '''
    try:
        # 获取用户id
        user_id=user_info['id']
        # 获取传参
        data=request.get_json()
        # 校验name和owner不能为空
        if not data.get('projectName') or not data.get('owner'):
            return jsonify(dict(code=101,msg='项目名称/项目负责人不能为空'))
        # 获取private，没获取到默认为False
        private=data.get('private',False)
        # 调用ProjectDao.add_project()新增项目
        err=ProjectDao.add_project(data.get('projectName'),data.get('owner'),user_id,data.get('description',''),private)
        # err不为None,新增失败，返回错误信息
        if err is not None:
            return jsonify(dict(code=100,msg=err))
        # 新增成功
        return jsonify(dict(code=0,msg='操作成功'))
    except Exception as e:
        return jsonify(dict(code=111,msg=str(e)))