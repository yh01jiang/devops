from flask import Flask,request,render_template

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref


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
创建Student类继承自db.Model类，
同时定义id、name、email、sex、....等属性，对应数据库中表的列
"""


class Student(db.Model):
    """学生信息模型"""
    # 声明与当前模型绑定的数据表名称
    __tablename__ = 't_1v1_student'
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(32),index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(128), unique=True, comment="邮箱")
    money = db.Column(db.Numeric(10, 2), default=0, comment="钱包")
    info = db.relationship('StudentInfo', uselist=False,backref='student')
    # 关联属性
    # 一般建议把关联属性放到主模型这里
    address_list = db.relationship('StudentAddress',uselist=True, backref="student", lazy="dynamic")

    def __repr__(self):
        """重写显示方法，定义之后，可以让显示对象的时候更直观"""
        return f"<{self.name} {self.__class__.__name__}>"


# 这个模型在这里暂时没用
class StudentInfo (db.Model):
    """ 学生附加信息表 """
    __tablename__ = 't_1v1_student_info'
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    # 外键字段提供给数据库
    student_id = db.Column(db.Integer, db.ForeignKey("t_1v1_student.id"), comment="student的外健")
    address = db.Column(db.String(255),index=True, comment="注册地址")
    mobile= db.Column(db.String(255),index=True, comment="注册地址")




    def __repr__(self):
        """重写显示方法，定义之后，可以让显示对象的时候更直观"""
        return f"<{self.student.name} {self.__class__.__name__}>"


class StudentAddress(db.Model):
    __tablename__ = 't_1vn_student_address'
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(50),default="默认", comment="地址名称")
    province = db.Column(db.String(50),comment="省份")
    city = db.Column(db.String(50),comment="城市")
    area = db.Column(db.String(50),comment="地区")
    address = db.Column(db.String(500),comment="详细地址")
    mobile =  db.Column(db.String(15),comment="收货人电话")
    #  外键字段提供给数据库
    student_id = db.Column(db.Integer, db.ForeignKey("t_1v1_student.id"), comment="student的外健")

    #关联属性
    # 外键模型 --> 主模型  StudentAddress.student 结果是一个模型对象
    # 主模型  --> 外键模型 Student.address_list 结果是一个列表
    # student = db.relationship('Student',uselist=False, backref=backref("address_list", uselist=True, lazy="dynamic"))

    def __repr__(self):
        """重写显示方法，定义之后，可以让显示对象的时候更直观"""
        return f"<{self.student.name} {self.__class__.__name__}>"



@app.route("/")
def index():
    """ 添加操作 """
    # 主模型已存在，添加外键模型
    student = Student(name="xiaohuang", age=16, sex=True, email="xiaohuang@qq.con", money=30000)
    db.session.add(student)
    db.session.commit()

    # 可以替换成下面的用法
    # student.address_list.append(StudentAddress(name="公司",province="北京",city="北京",area="西城区",address="百沙路201号",mobile="13312345678"))
    # db.session.commit()


    student.address_list = [
        StudentAddress(name="公司",province="北京",city="北京",area="西城区",address="百沙路201号",mobile="13312345678"),
        StudentAddress(name="公司",province="北京",city="北京",area="西城区",address="百沙路202号",mobile="13312345678"),
        StudentAddress(name="公司",province="北京",city="北京",area="西城区",address="百沙路203号",mobile="13312345678"),
    ]
    
    db.session.commit()

    # 添加主模型的同时，添加附加外键模型
    student = Student(
        name="xiaohei",
        age=22,
        sex=True,
        email="xiaohei@qq.com",
        money=20000,
        address_list=[
            StudentAddress(name="公司",province="北京",city="北京",area="西城区",address="百沙路301号",mobile="18812345678"),
            StudentAddress(name="公司",province="北京",city="北京",area="西城区",address="百沙路302号",mobile="18812345678"),
            StudentAddress(name="公司",province="北京",city="北京",area="西城区",address="百沙路303号",mobile="18812345678"),
        ]
    )
    db.session.add(student)
    db.session.commit()

    # 添加外键模型的同时，添加主模型（不推荐）
    address = StudentAddress(
        name="家里",
        province="上海市",
        city="上海市",
        area="浦东新区",
        address="浦东新区建豪路100号",
        mobile="133335432189",
        student = Student(
            name = "lixiaolan",
            age = "99",
            sex = False,
            email = "lixiaolan@qq.com",
            money = 77777,
        )
    )
    db.session.add(address)
    db.session.commit()


    """ 查询操作 """
    student = Student.query.filter(Student.name == "xiaohuang").first()
    print(student.address_list.all())





    return "ok"




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

