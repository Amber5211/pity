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

@pr.route('/query')
@permission()
def query_project(user_info):
    '''
    根据project_id获取项目详情
    :param user_info:
    :return:
    '''
    project_id=request.args.get('projectId')
    print(project_id)
    if project_id is None or not project_id.isdigit():
        return jsonify(dict(code=101,msg='请传入正确的project_id'))

    data,roles,err=ProjectDao.query_project(project_id)
    result=dict()
    if err is not None:
        return jsonify(dict(code=110,data=result,msg=err))

    result.update({"project":ResponseFactory.model_to_dict(data),"roles":ResponseFactory.model_to_list(roles)})

    return jsonify(dict(code=0,data=result,msg='操作成功'))


@pr.route('/update',methods=['POST'])
@permission()
def update_project(user_info):
    '''
    更新项目信息
    :param user_info:
    :return:
    '''
    try:
        # 获取user_id,role
        user_id,role=user_info['id'],user_info['role']
        # 获取请求参数
        data=request.get_json()
        # 校验项目id不能为空
        if data.get('id') is None:
            return jsonify(dict(code=101,msg='项目id不能为空'))
        # 校验项目名称和项目负责人不能为空
        if data.get('name') is None or data.get('owner') is None:
            return jsonify(dict(code=101,msg='项目名称/项目负责人不能为空'))

        private=data.get('private',False)
        # 调用ProjectDao.update_project方法更新项目信息
        err=ProjectDao.update_project(user_id,role,data.get('id'),data.get('name'),data.get('owner'),private,data.get('description',''))

        if err is not None:
            return jsonify(dict(code=0,msg=err))

        return jsonify(dict(code=0,msg='操作成功'))


    except Exception as e:
        return jsonify(dict(code=111,msg=str(e)))
