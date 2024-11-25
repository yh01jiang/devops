import db
from datetime import datetime


# 1. 创建一个与数据库对应的模型类对象
class Student(db.Model):
    """学生表模型"""
    # 1. 把当前模型与数据库中指定的表名进行关联
    __tablename__ = "tb1_student"

    # 2. 绑定字段信息
    # 模型属性 = db.Column(数据类型, 字段约束)
    # primary_key=True 设置当前字段为整型，主键，SQLAlchemy会自动设置auto_increment为自增
    id = db.Column(db.Integer, primary_key=True)
    # db.String(20) 设置当前字段为字符串，varchar(20)
    name = db.Column(db.String(20))
    # db.Boolean 设置当前字段为布尔类型，本质上在数据库中是 0/1
    # default=True 设置当前字段的默认值
    sex = db.Column(db.Boolean, default=True)
    age = db.Column(db.SmallInteger)
    # 当前字段名如果是python关键字，则需要给第一个参数则字段的别名使用
    # SmallInteger = SMALLINT
    classes = db.Column("class", db.SMALLINT)
    # Text 表示设置当前字段为文本格式，因为文本与字符串varchar在python都是字符串，所以此处可以兼容
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=1)
    # DateTime 设置字段为日期时间类型
    # 注意：如果设置当前日期时间为默认值，不能在now加上小括号
    addtime = db.Column(db.DateTime, default=datetime.now)
    orders = db.Column(db.SMALLINT, default=1)


if __name__ == '__main__':
    # 如果没有提前声明模型中的数据表，则可以采用以下代码生成新的数据表，这个操作叫数据迁移
    # 如果数据库中已经声明了有数据表，则不会继续生成新的数据表
    # db.Model.metadata.drop_all(db.engine)
    db.Model.metadata.create_all(db.engine)




"""
数据迁移：
基于上面初始化模型，创建模型，如果模型绑定的数据表不存在，则自动创建数据表。

数据表存在，则不会新建，这个过程称之为数据迁移。
"""

"""

以后为了方便管理，把数据库连接部分放单独的py文件中，在这里使用import 导进来
"""