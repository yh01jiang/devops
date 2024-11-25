from flask import Flask,request,render_template

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
    # 关联属性[提供给SQLAlchemy], 关联属性的声明，可以在两个关联模型中任意一个模型里面
    # db.relationship意义就是使用Student.info 可以查询到StudentInfo的数据
    # backref='student'  可以使用StudentInfo.student查询到Student的数据 
    info = db.relationship('StudentInfo', uselist=False,backref='student')

    def __repr__(self):
        """重写显示方法，定义之后，可以让显示对象的时候更直观"""
        return f"<{self.name} {self.__class__.__name__}>"


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




@app.route("/")
def index():
    """ 一对一 的添加 """
    """ 第一种：添加主模型的同时也添加外键模型(2个数据都是新增的)"""
    student = Student(
        name= "xiaohuang",
        age = 13,
        sex = True,
        email = "xiaohuang@qq.com",
        money = 1000,
        info = StudentInfo(
            mobile="13312345678",
            address="北京市昌平区白沙路103号"
        )
    )
    db.session.add(student)
    db.session.commit()

    """ 第二种： 已经有了主模型，基于主模型新增外键模型 """
    student = Student(name="xiaobai", age=18, sex=False, email="xiaobai@qq.com", money=2000)
    db.session.add(student)
    db.session.commit()

    student.info = StudentInfo(address="北京朝阳", mobile="18712345678")
    db.session.commit()


    """ 第三种：添加外键模型时添加主模型 （很少用）"""
    info = StudentInfo(
        mobile="18312345678",
        address="上海浦东",
        student = Student(
            name= "xiaohei",
            age = 24,
            sex = True,
            email = "xiaohei@qq.com",
            money = 1800,
            )
    )
    db.session.add(info)
    db.session.commit()

    return "ok"

@app.route("/data")
def data():
    """ 查询操作 """
    """ 以外键模型的字段作为主模型的查找条件 """
    student = Student.query.filter(StudentInfo.mobile=="13312345678").first()
    print(student)

    """ 以主键模型的字段作为外键模型的查找条件"""
    student = StudentInfo.query.filter(Student.name=="xiaohuang").first()
    print(student.mobile)

    """ 通过主模型调用外键模型"""
    student = Student.query.filter(Student.name=="xiaobai").first()
    print(student.info)
    print(student.info.mobile)

    """通过外键模型调用主模型"""
    info = StudentInfo.query.filter(StudentInfo.mobile=="13312345678").first()
    print(info.student)
    print(info.student.name)

    """ 更新操作 """
    # 根据主模型修改附加模型的数据
    student1 = Student.query.filter(Student.name == "xiaohei").first()
    student1.age = 222
    student1.info.address = "上海浦西222"
    db.session.commit()

    # 根据外键模型修改主模型的数据
    info = StudentInfo.query.filter(StudentInfo.mobile == "13312345678").first()
    info.student.age= 10
    db.session.commit()

    """ 删除操作 """
    # 删除主模型,SQlAlchemy会自动把对应的外键字段值设置Null
    student = Student.query.get(3)
    db.session.delete(student)
    db.session.commit()

    # 删除附加模型,则直接删除，则不会删除主模型
    info = StudentInfo.query.get(2)
    db.session.delete(info)
    db.session.commit()

    return "ok"



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

