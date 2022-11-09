from app.models import db
from datetime import datetime


class User(db.Model):
    id=db.Column(db.INT,primary_key=True,comment='自增主键')
    username=db.Column(db.String(16),unique=True,index=True,comment='用户名')
    name=db.Column(db.String(16),index=True,comment='姓名')
    password=db.Column(db.String(32),comment='密码')
    email=db.Column(db.String(64),unique=True,nullable=False,comment='邮箱')
    role=db.Column(db.INT,default=0,comment='角色 0:普通用户 1:组长 2:超级管理员')
    created_at=db.Column(db.DATETIME,nullable=False,comment='创建时间')
    updated_at = db.Column(db.DATETIME, nullable=False,comment='更新时间')
    deleted_at=db.Column(db.DATETIME,comment='删除时间')
    last_login_at=db.Column(db.DATETIME,comment='最后登录时间')


    def __init__(self,username,name,password,email):
        self.username=username
        self.name=name
        self.password=password
        self.email=email
        self.role=0
        self.created_at=datetime.now()
        self.updated_at=datetime.now()

    # 格式化返回类的名称
    def __repr__(self):
        return '<User %r>' % self.username