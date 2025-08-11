from flask import Flask,request,render_template

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

from flask_migrate import Migrate


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

# 把数据迁移绑定到当前的应用对象中，与SQLAlchemy的数据库ORM模块进行关联
migrate = Migrate()
migrate.init_app(app, db)

""" 
创建Student类继承自db.Model类，
同时定义id、name、email、sex、....等属性，对应数据库中表的列
"""


class Student(db.Model):
    """学生信息模型"""
    # 声明与当前模型绑定的数据表名称
    __tablename__ = 't_migrate_student'
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(32),index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(128), unique=True, comment="邮箱")
    money = db.Column(db.Numeric(10, 2), default=0, comment="钱包")
    info = db.relationship('StudentInfo', uselist=False,backref='student')

    def __repr__(self):
        """重写显示方法，定义之后，可以让显示对象的时候更直观"""
        return f"<{self.name} {self.__class__.__name__}>"


# 这个模型在这里暂时没用
class StudentInfo (db.Model):
    """ 学生附加信息表 """
    __tablename__ = 't_migrate_studentinfo'
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    # 外键字段提供给数据库
    student_id = db.Column(db.Integer, db.ForeignKey("t_1v1_student.id"), comment="student的外健")
    address = db.Column(db.String(255),index=True, comment="注册地址")
    mobile= db.Column(db.String(255),index=True, comment="注册地址")




    def __repr__(self):
        """重写显示方法，定义之后，可以让显示对象的时候更直观"""
        return f"<{self.student.name} {self.__class__.__name__}>"


class StudentAddress(db.Model):
    __tablename__ = 't_mirgate_address'
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(50),default="默认", comment="地址名称")
    province = db.Column(db.String(50),comment="省份")
    city = db.Column(db.String(50),comment="城市")
    area = db.Column(db.String(50),comment="地区")
    address = db.Column(db.String(500),comment="详细地址")
    mobile =  db.Column(db.String(15),comment="收货人电话")
    #  外键字段提供给数据库
    student_id = db.Column(db.Integer, db.ForeignKey("t_1v1_student.id"), comment="student的外健")


    def __repr__(self):
        """重写显示方法，定义之后，可以让显示对象的时候更直观"""
        return f"<{self.student.name} {self.__class__.__name__}>"



@app.route("/")
def index():
    
    return "ok"




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)