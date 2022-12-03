from sqlalchemy import or_

from app import pity
from app.models import db
from app.models.project import Project
from app.dao.project.ProjectRoleDao import ProjectRoleDao
from app.utils.logger import Log


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
                project_list=ProjectRoleDao.list_project_by_user(user)
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
            return 0,0,f"获取用户:{user}项目列表失败,{e}"

    @staticmethod
    def add_project(name,owner,user,private):
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
            if data is None:
                return '项目已存在'
            #新增项目
            pr=Project(name,owner,user,private)
            db.session.add(pr)
            db.session.commit(pr)

        except Exception as e:
            ProjectDao.log.error(f"新增项目:{name}失败,{e}")
            return 0,0,f"新增项目:{name}失败,{e}"



