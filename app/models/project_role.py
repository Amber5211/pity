from app.models import db
from datetime import datetime

# 项目角色表
class ProjectRole(db.Model):
    id=db.Column(db.INT,primary_key=True,comment='主键id')
    user_id=db.Column(db.INT,index=True,comment='用户id')
    project_id=db.Column(db.INT,index=True, comment='项目id')
    project_role=db.Column(db.INT,index=True, comment='项目角色 1: 组长 2: 组员')
    created_at = db.Column(db.DATETIME, nullable=False, comment='创建时间')
    updated_at = db.Column(db.DATETIME, nullable=False, comment='更新时间')
    deleted_at = db.Column(db.DATETIME, comment='删除时间')
    create_user = db.Column(db.INT, nullable=True, comment='创建人')
    update_user = db.Column(db.INT, nullable=True, comment='更新人')

    def __init__(self,user_id,project_id,project_role,create_user):
        self.user_id=user_id
        self.project_id=project_id
        self.project_role=project_role
        self.created_at=datetime.now()
        self.updated_at=datetime.now()
        self.create_user=create_user
        self.update_user=create_user
        self.deleted_at=None