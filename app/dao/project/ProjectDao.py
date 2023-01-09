from sqlalchemy import or_

from app import pity
from app.models import db
from app.models.project import Project
from app.dao.project.ProjectRoleDao import ProjectRoleDao
from app.utils.logger import Log

from datetime import datetime


class ProjectDao(object):
    log=Log("ProjectDao")

    @staticmethod
    def list_project(user,role,page,size,name=None):
        '''
        查询/获取项目列表
        :param user: 当前用户
        :param role: 当前用户角色
        :param page: 当前页码
        :param size: 当前size
        :param name: 项目名称
        :return:
        '''
        try:
            search=[Project.deleted_at== None]#定义查询条件的列表，filter查询参数匹配是“==”
            # 判断用户role是否是管理员,不是管理员查询用户所拥有的项目和owner为当前用户，private为私有的项目
            if role != pity.config.get("ADMIN"):
                project_list,err=ProjectRoleDao.list_project_by_user(user)
                # 如果返回异常，抛出异常
                if err is not None:
                    raise err
                search.append(or_(Project.id in project_list, Project.owner==user,Project.private==False))
            #有name参数，把name参数加入到询条件列表
            if name:
                search.append(Project.name.like(f"%{name}%"))
            # 根据查询条件查询项目数据
            data=Project.query.filter(*search)
            total=data.count()
            # 分页返回项目数据，.items是获取paginate返回对象的分页数据记录items
            return data.order_by(Project.created_at.desc()).paginate(page,per_page=size).items,total,None

        except Exception as e:
            ProjectDao.log.error(f"获取用户:{user}项目列表失败,{e}")
            return [],0,f"获取用户:{user}项目列表失败,{e}"

    @staticmethod
    def add_project(name,owner,user,description,private):
        '''
        新增项目
        :param name: 项目名
        :param owner: 组长
        :param user: 创建人
        :param private: 是否私有
        :return:
        '''

        try:
            # 查询项目是否已存在
            data=Project.query.filter_by(name=name,deleted_at=None).first()
            if data is not None:
                return '项目已存在'
            #新增项目
            pr=Project(name,owner,user,description,private)
            db.session.add(pr)
            db.session.commit()

        except Exception as e:
            ProjectDao.log.error(f"新增项目:{name}失败,{e}")
            return f"新增项目:{name}失败,{e}"

        return None

    @staticmethod
    def query_project(project_id:int):
        '''
        根据项目id获取项目的详情信息
        :param project_id: 项目id
        :return:
        '''
        try:
            # 根据project_id查询Project表
            data=Project.query.filter_by(id=project_id,deleted_at=None).first()
            # 为空，返回项目不存在
            if data is None:
                return None,[],'项目不存在'
            # 根据project_id查询ProjectRole表
            roles,err=ProjectRoleDao.list_role(project_id)
            # 未查询到项目角色，返回空和err
            if err is not None:
                return None,[],err
            # 返回data（Project数据），roles（ProjectRole数据）
            return data,roles,None
        except Exception as e:
            # 查询报错，返回错误信息
            ProjectDao.log.error(f"查询项目：{project_id}详情失败，{e}")
            return None,[],f"查询项目：{project_id}详情失败，{e}"


    @staticmethod
    def update_project(user,role,project_id,name,owner,private,description):
        '''
        更新项目信息
        :param user: 用户id
        :param role: 用户角色
        :param project_id: 项目id
        :param name: 项目名称
        :param owner: 组长
        :param private: 是否私有
        :param description: 描述
        :return:
        '''
        try:
            # 查询修改的项目是否存在
            data=Project.query.filter_by(id=project_id,deleted_at=None).first()
            if data is None:
                return '项目不存在'

            # 校验用户是否有修改项目的权限，权限为管理员或者用户为项目的负责人才可以修改
            if role < pity.config.get("ADMIN") or user !=data.owner:
                return '您没有权限修改项目负责人'

            data.name = name
            data.private = private
            data.description = description
            data.updated_at = datetime.now()
            data.update_user = user
            db.session.commit()

        except Exception as e:
            ProjectDao.log.error(f"编辑项目:{name}失败，{e}")
            return f"编辑项目:{name}失败，{e}"

        return None



