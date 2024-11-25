from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 连接数据库url（python3环境）
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456789@127.0.0.1:3306/school?charset=utf8"
# 动态追踪对象修改并且发送信号，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 查询时会显示原始sql语句
app.config["SQLALCHEMY_ECHO"] = True


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
    """ 添加1条数据 """
    # student = Student(
    #     name = "xiaoming",
    #     age = 17,
    #     sex = True,
    #     email = "xiaoming@qq.com",
    #     money = 30.50
    # )
    # db.session.add(student)
    # db.session.commit()

    """ 添加多条数据 """
    # student_list = [
    #     Student(name="小黑", age=16, sex=True, email="xiaohei@qq.com", money=100),
    #     Student(name="小白", age=21, sex=True, email="xiaobai@qq.com", money=2000),
    #     Student(name="小红", age=43, sex=False, email="xiaohong@qq.com", money=600),
    #     Student(name="小绿", age=27, sex=True, email="xiaolv@qq.com", money=4000),
    #     Student(name="小蓝", age=18, sex=False, email="xiaolan@qq.com", money=800),
    # ]

    # db.session.add_all(student_list)
    # db.session.commit()

    """ 更新操作 """
    # # 更新1条数据
    # student = Student.query.get(3)
    # student.age = 18
    # db.session.commit()

    """ 更新多条数据 """
    # Student.query.filter(Student.sex == True).update({Student.money: Student.money+100})
    # db.session.commit()

    """ 删除1条数据 """
    # student = Student.query.get(5)
    # db.session.delete(student)
    # db.session.commit()

    """ 删除多条数据 """
    Student.query.filter(Student.sex == False).delete()
    db.session.commit()

    return "ok"


if __name__ == '__main__':
    with app.app_context():
        # 如果没有提前声明模型中的数据表，则可以采用以下代码生成数据表结构
        # 如果数据库中已经声明了有数据表，则不会继续生成。
        db.create_all()
    app.run(debug=True)

