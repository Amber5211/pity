from datetime import datetime

class ResponseFactory(object):

    @staticmethod
    def model_to_dict(obj,*ignore:str):
        '''
        model对象转换成字典
        :param obj: model对象
        :param ignore: 忽略字段
        :return: data
        '''
        data=dict()

        for c in obj.__table__.columns:#obj.__table__.columns:数据库表对象的各个列
            if c.name in ignore:
                # 如果字段是忽略字段，则不进行转换
                continue
            # 获取属性值
            val=getattr(obj,c.name)
            # 判断属性值是否是datetime类型
            if isinstance(val,datetime):
                # datetime类型格式化字符串类型
                data[c.name]=val.strftime("%Y-%m-%d %H:%M:%S")
            else:
                data[c.name]=val
        return data

    @staticmethod
    def model_to_list(data:list,*ignore:str):
        '''
        model对象列表，转换成字典列表
        :param data: model对象列表
        :param ignore: 忽略字段
        :return: list
        '''
        return [ResponseFactory.model_to_dict(x,*ignore) for x in data]