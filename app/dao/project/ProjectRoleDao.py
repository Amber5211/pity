from app.models import db
from app.models.project_role import ProjectRole
from app.utils.logger import Log



class ProjectRoleDao(object):
    log=Log("ProjectRoleDao")


    @staticmethod
    def list_project_by_user(user_id):
        '''
        通过user_id获取项目列表
        :param user_id: 用户id
        :return:
        '''
        try:
            projects=ProjectRole.query.filter_by(user_id=user_id,deleted_at=None).all()
            return [p.id for p in projects],None
        except Exception as e:
            ProjectRoleDao.log.error(f"查询用户：{user_id}项目失败,{e}")
            return [],f"查询项目失败，{e}"


    @staticmethod
    def add_project_role(user_id,project_id,project_role,user):
        '''
        项目添加用户
        :param user_id:用户id
        :param project_id:项目id
        :param project_role:用户角色
        :param user:创建人
        :return:
        '''
        try:
            role=ProjectRole.query.filter_by(user_id=user_id,project_id=project_id,project_role=project_role,deleted_at=None).first()

            if role is not None:
                # 说明用户已存在该项目
                return '该用户已存在'

            # 添加项目用户
            role=ProjectRole(user_id,project_id,project_role,user)
            db.session.add(role)
            db.session.commit()

        except Exception as e:
            ProjectRoleDao.log.error(f"添加项目用户失败,{e}")
            return f"添加项目用户失败,{e}"

        return None

    @staticmethod
    def list_role(project_id:int):
        '''
        根据项目id获取项目的角色
        :param project_id:项目id
        :return:
        '''
        try:
            # 根据project_id查询ProjectRole表数据
            roles=ProjectRole.query.filter_by(project_id=project_id,deleted_at=None).all()

            return roles,None

        except Exception as e:
            # 查询失败，返回错误信息
            ProjectRoleDao.log.error(f"查询项目：{project_id}角色列表失败，{e}")
            return [],f"查询项目：{project_id}角色列表失败，{e}"