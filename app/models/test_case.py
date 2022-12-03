from app.models import db
from datetime import datetime

# 项目角色表
class TestCase(db.Model):
    id=db.Column(db.INT,primary_key=True,comment='主键id')
    name=db.Column(db.String(32),unique=True,index=True, comment='用例名称')
    request_type=db.Column(db.INT,default=1,comment='请求类型 1:http 2:grpc 3:dubbo')
    url=db.Column(db.TEXT,nullable=False,comment='请求url')
    request_method=db.Column(db.String(12),nullable=True,comment="请求方式，如果非http可为空")
    request_header = db.Column(db.TEXT, comment="请求头，可为空")
    params=db.Column(db.TEXT,comment="请求params")
    body=db.Column(db.TEXT,comment='请求body')
    project_id = db.Column(db.INT, comment="所属项目")
    tag = db.Column(db.String(64), comment="用例标签")
    status = db.Column(db.INT, comment="用例状态: 1: 待完成 2: 暂时关闭 3: 正常运作")
    expected = db.Column(db.TEXT,nullable=False,comment="预期结果, 支持el表达式")
    created_at = db.Column(db.DATETIME, nullable=False, comment='创建时间')
    updated_at = db.Column(db.DATETIME, nullable=False, comment='更新时间')
    deleted_at = db.Column(db.DATETIME, comment='删除时间')
    create_user = db.Column(db.INT, nullable=False, comment='创建人')
    update_user = db.Column(db.INT, nullable=False, comment='更新人')

    def __init__(self, name, request_type, url, project_id, tag, status, expected, create_user, request_header=None,
                 request_method=None):
        self.name = name
        self.request_type = request_type
        self.url = url
        self.project_id = project_id
        self.tag = tag
        self.status = status
        self.expected = expected
        self.create_user = create_user
        self.update_user = create_user
        self.request_header = request_header
        self.request_method = request_method
        self.created_at = datetime.now()
        self.updated_at = datetime.now()