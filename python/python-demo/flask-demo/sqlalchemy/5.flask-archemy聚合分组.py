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
    # """ 聚合函数 """
    # from sqlalchemy import func

    # # 获取所有学生的money总数
    # ret = db.session.query(func.sum(Student.money)).first()[0]
    # print(ret)
   
    # # scalar() 这个比first()[0] 更友好
    # ret = db.session.query(func.sum(Student.money)).scalar()
    # print(ret)

    # # 查询女生的数量
    # ret = db.session.query(func.count(Student.id)).filter(Student.sex==False).scalar()
    # print(ret)

    # # 查询所有学生的平均年龄
    # ret = db.session.query(func.avg(Student.age)).scalar()
    # print(ret)

    # """分组查询 """
    # # 查询男生女生的平均年龄
    # ret = db.session.query(func.avg(Student.age)).group_by(Student.sex).all()
    # print(ret)

    # # 查询各个年龄段的学生数量
    # # 分组时： db.session.query()中的字段，只能要么是被分组的子段，要么是聚合结果
    # ret = db.session.query(Student.age, func.count(Student.id)).group_by(Student.age).all()
    # print(ret)

    # # 多字段分组
    # # 查询各个年龄段的女生余男生的数量
    # ret = db.session.query(Student.age, Student.sex, func.count(Student.id)).group_by(Student.age,Student.sex).all()
    # print(ret)

    # # 分组后的过滤操作（having）
    # # 在所有学生中，找出各个年龄中拥有最多钱的同学，并在这些学生中筛选出money > 1000的数据

    # subquery = func.max(Student.money)
    # ret = db.session.query(Student.age, subquery).group_by(Student.age).having(subquery > 1000 ).all()
    # print(ret)


    """ 执行原生SQL语句 """
    # 查询多条语句
    ret = db.session.execute("select * from tb_student").fetchall()
    print(ret)

    # 查询一条语句
    ret = db.session.execute("select * from tb_student").fetchone()
    print(ret)


    return "ok"


if __name__ == '__main__':
    with app.app_context():
        # 如果没有提前声明模型中的数据表，则可以采用以下代码生成数据表结构
        # 如果数据库中已经声明了有数据表，则不会继续生成。
        db.create_all()
    app.run(debug=True)

