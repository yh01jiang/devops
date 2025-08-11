from flask import Flask,request,render_template

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 连接数据库url（python3环境）
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456789@127.0.0.1:3306/school?charset=utf8"
# 动态追踪对象修改并且发送信号，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# 查询时会显示原始sql语句
app.config["SQLALCHEMY_ECHO"] = False


# 实例化得到对象db，把SQLALCHEMY组件(db)注册app中,  
""" 这两可以合并为： db = SQLAlchemy(app) """
db = SQLAlchemy()
db.init_app(app)

# print(dir(db))


""" 
创建User类继承自db.Model类，
同时定义id、name、email、sex、....等属性，对应数据库中表的列
"""


class Student(db.Model):
    """学生信息模型"""
    """
    CREATE TABLE tb_student (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT, 
        name VARCHAR(32) COMMENT '姓名', 
        age SMALLINT COMMENT '年龄', 
        sex BOOL COMMENT '性别', 
        email VARCHAR(128) COMMENT '邮箱', 
        money NUMERIC(10, 2) COMMENT '钱包', 
        PRIMARY KEY (id), 
        UNIQUE (email)
)
    """
    # 声明与当前模型绑定的数据表名称
    __tablename__ = 'tb_student'
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(32),index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(128), unique=True, comment="邮箱")
    money = db.Column(db.Numeric(10, 2), default=0, comment="钱包")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"

class Course(db.Model):
    """ 课程模型 """
    """
    CREATE TABLE tb_course (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT, 
        name VARCHAR(32) COMMENT '姓名', 
        price NUMERIC(8, 2) COMMENT '价格', 
        PRIMARY KEY (id), 
        UNIQUE (name)
)
    """
    __tablename__ = 'tb_course'
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(32),unique=True, comment="姓名")
    price = db.Column(db.Numeric(8,2), comment="价格")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"
    
class Teacher(db.Model):
    """ 老师模型 """
    """
    CREATE TABLE tb_teacher (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT, 
        name VARCHAR(255) COMMENT '姓名', 
        `option` ENUM('讲师','助教','班主任'), 
        PRIMARY KEY (id), 
        UNIQUE (name)
)
    """
    __tablename__ = 'tb_teacher'
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255),unique=True, comment="姓名")
    option = db.Column(db.Enum("讲师", "助教", "班主任",), default="讲师")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"




@app.route("/data")
def data():
    # """模糊查询"""
    # # 名字以小开头的名字
    # student = Student.query.filter(Student.name.startswith('小')).all()
    # print(student)

    # # 名字以白结尾的名字
    # student = Student.query.filter(Student.name.endswith('白')).all()
    # print(student)

    # # 名字包含ming字的学生
    # student = Student.query.filter(Student.name.contains('ming')).all()
    # print(student)

    # """ 比较查询 """
    # # 格式为: filter(模型.字段 比较运算符 值)
    # # ⽐较运算符：>、<、>=、<=、!=、==
    # # 单条件查询
    # studeng_list = Student.query.filter(Student.age>15).all()
    # print(studeng_list)

    # # 多条件查询
    # # 要是多个条件满足，相当于and
    # student = Student.query.filter(Student.sex==True, Student.age> 16).all()
    # print(student)


    # """ filter_by 精确查询 """
    # # filter_by只支持字段的值是否相等的情况，对于大于 小于 大于等于 等等其他条件是不支持的 
    # # 单条件: filter_by(字段=值)
    # # 多条件: filter_by(字段=值, 字段=值, 字段=值)
    # student = Student.query.filter_by(age =16).all()
    # print(student)

        


    # """ 逻辑查询 """
    # # 其实一般情况下，我们使用filter(条件1, 条件2) 使用逗号就代表的是与

    # # 逻辑与
    # # filter(and_(条件1,条件2)) 等价于 filter(条件1, 条件2, ...)
    # from sqlalchemy import and_
    # student_list = Student.query.filter(and_(Student.age>16, Student.sex==False)).all()
    # print(student_list)
   
    # # 逻辑或
    # # 查询年龄大于16或者钱包余额大于100  女生
    # from sqlalchemy import or_
    # student_list = Student.query.filter(or_(Student.age>16, Student.money> 100), Student.sex==False).all()
    # print(student_list)

    # # 查询年龄大于16的男生和钱包余额大于100的女生
    # from sqlalchemy import or_, and_
    # student_list = Student.query.filter(
    #     or_(
    #         and_(Student.age>16,Student.sex==True), 
    #         and_(Student.money> 100, Student.sex==False)
    #         )
    #     ).all()
    # print(student_list)


    # """ 逻辑非 """
 
    # student = Student.query.filter(Student.name != "小白").all()
    # print(student)

    # from sqlalchemy import not_
    # student_list = Student.query.filter(not_(Student.name=="小白")).all()
    # print(student_list)


    # """ 检查是否存在某个数据 """

    # user_exists = db.session.query(Student.query.filter_by(name="小白").exists()).scalar()
    # print(user_exists)

    
    # student = Student.query.filter(Student.name=="小白").first()
    # print(bool(student))



    # """ in 范围查询 """
    # #查询id在[1,3,4,5]
    # student = Student.query.filter(Student.id.in_([1,3,4,5])).all()
    # print(student)

    # """ is 判断"""
    # # 查询邮箱为None的用户
    # studengt_list = Student.query.filter(Student.email.is_(None)).all()
    # print(studengt_list)

    # """ order by 排序"""
    # # 按年龄排序
    # # student = Student.query.order_by(Student.age.desc()).all()
    # # print(student)

    # # 按钱包余额倒序,如果余额一致，按照id进行正序
    # student_list = Student.query.order_by(Student.money.desc(), Student.id.asc()).all()
    # print(student_list)

    # """ offset偏移量 与限制 """
    # # 查询年龄最大的3个人
    # student = Student.query.order_by(Student.age.desc()).limit(3).all()
    # print(student)

    # # 查询钱包余额最少的3个人
    # student_list = Student.query.order_by(Student.money.asc()).limit(3).all()
    # print(student_list)

    # # 按钱包余额进行倒序排列，查询出排名在4-6之间的学生
    # student = Student.query.order_by(Student.money.desc()).offset(3).all()
    # print(student)

    # student = Student.query.order_by(Student.money.desc()).offset(3).limit(2).all()
    # print(student)

    # student = Student.query.order_by(Student.money.desc()).all()[3:5]
    # print(student)

    """ 分页器 """
    # student_list = Student.query.all()
    # print(student_list)

    # 分页器对象 = 模型.query.filter(过滤条件).paginate(page=页码, per_page=单页数据量, max_per_page=最大分页数)
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 5))

    pagination = Student.query.paginate(page=page, per_page=size)

    # print(pagination)

    # print(pagination.total)  # 总数据量
    # print(pagination.items)  # 当前页的数据
    # print(pagination.pages)  # 总页码
    # print(pagination.page)  # 当前页码

    # print(pagination.prev)  # 上一页分页器对象
    # print(pagination.has_prev)  # 是否有上一页
    # print(pagination.prev_num)  # 是否有上一页
    # print(pagination.prev().items)  # 上一页展示的数据列表

    # print(pagination.next)  # 上一页分页器对象
    # print(pagination.has_next)  # 是否有上一页
    # print(pagination.next_num)  # 是否有上一页
    # print(pagination.next().items)  # 上一页展示的数据列表


    """ 前后端分离 """
    # data = {
    #     "page": pagination.page,
    #     "pages": pagination.pages,
    #     "has_prev": pagination.has_prev,
    #     "prev_num": pagination.prev_num,
    #     "has_next": pagination.has_next,
    #     "next_num": pagination.next_num,
    #     "items": [{
    #         "id": item.id,
    #         "name": item.name,
    #         "age": item.age,
    #         "sex": item.sex,
    #         "money": item.money

    #     } for item in pagination.items]
    # }
    # return data


    """ 前后端不分离 """
    return render_template("list1.html", **locals())
    


if __name__ == '__main__':
    with app.app_context():
        # 如果没有提前声明模型中的数据表，则可以采用以下代码生成数据表结构
        # 如果数据库中已经声明了有数据表，则不会继续生成。
        db.create_all()
    app.run(debug=True)

