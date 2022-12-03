from app.models import db
from datetime import datetime

# 项目表
class Project(db.Model):
    id=db.Column(db.INT,primary_key=True,comment='主键id')
    name=db.Column(db.String(16),unique=True,index=True,comment='项目名')
    owner=db.Column(db.INT,comment='组长')
    created_at=db.Column(db.DATETIME,nullable=False,comment='创建时间')
    updated_at = db.Column(db.DATETIME, nullable=False, comment='更新时间')
    deleted_at = db.Column(db.DATETIME, comment='删除时间')
    create_user=db.Column(db.INT,nullable=True, comment='创建人')
    update_user=db.Column(db.INT,nullable=True, comment='更新人')
    private=db.Column(db.BOOLEAN,default=False, comment='是否私有')

    def __init__(self,name,owner,create_user,private=False):
        self.name=name
        self.owner=owner
        self.private=private
        self.created_at=datetime.now()
        self.updated_at=datetime.now()
        self.create_user=create_user
        self.update_user=create_user
        self.deleted_at=None