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

# 关系表(这种表无法给flask进行操作的，仅仅用于在数据库中记录两个模型之间的关系)
student_course_table = db.Table(
    "t_nvm_student_course",
    db.Column("id", db.Integer, primary_key=True, comment="主键ID"),
    db.Column("sid", db.Integer, db.ForeignKey("t_nvm_student.id"), comment="学生ID"),
    db.Column("cid", db.Integer, db.ForeignKey("t_nvm_course.id"), comment="课程表ID"),

)


class Student(db.Model):
    """学生信息模型"""
    __tablename__ = 't_nvm_student'
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(32),index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(128), unique=True, comment="邮箱")
    money = db.Column(db.Numeric(10, 2), default=0, comment="钱包")
    # 只有设置关联属性以后，flask中才提供模型关联的操作
    # secondary 代表第三方的表明的返回值（student_course_table），说白了就是代表的是关系。
    course_list = db.relationship('Course', secondary=student_course_table, backref="student_list", lazy="dynamic")

    def __repr__(self):
        """重写显示方法，定义之后，可以让显示对象的时候更直观"""
        return f"<{self.name} {self.__class__.__name__}>"
    




class Course(db.Model):
    """课程信息模型"""
    __tablename__ = 't_nvm_course'
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="课程")
    

    def __repr__(self):
        """重写显示方法，定义之后，可以让显示对象的时候更直观"""
        return f"<{self.name} {self.__class__.__name__}>"




@app.route("/")
def index():
    """ 添加数据 """
    # # 添加其中一个主模型数据时，同时绑定添加另外一个主模型的数据，这个过程中，关系表会自动写入2者的关系数据，绑定2个模型之间的关系
    # student = Student(
    #     name="xiaozhao",
    #     age=13,
    #     sex=False,
    #     email= "xiaozhao@qq.com",
    #     money=1000,
    #     course_list=[
    #         Course(name="python入门"),
    #         Course(name="python初级"),
    #         Course(name="python进阶"),
    #     ]
    # )
    # db.session.add(student)
    # db.session.commit()

    # # 在已有课程模型的基础上，新增学生，新增报读课程。

    # student = Student(
    #     name="xiaohong",
    #     age=14,
    #     sex=False,
    # )
    # db.session.add(student)
    # db.session.commit()
    
    # student = Student.query.filter(Student.name == "xiaohong").first()
    # # 让小红新增报读课程id为3的课程
    # student.course_list.append(Course.query.get(3))
    # student.course_list.append(Course(name="python高级"))
    # db.session.commit()

    #让学生一次性报读多个已有课程

    # student1 = Student.query.get(2)
    # course_list = Course.query.filter(Course.id.in_([1,2])).all()
    # student1.course_list.extend(course_list)
    # db.session.commit()

    # # 查询id为1的学生购买的课程
    # student = Student.query.get(1)
    # print(student.course_list.all())

    # # 查询id为4的课程，有哪些学生购买了
    # course = Course.query.get(4)
    # print(course.student_list)


    """更新数据"""
    # # 给报读了4号课程的同学，返现红包200块钱
    # course = Course.query.get(4)
    # for student in course.student_list:
    #     student.money += 200
    # db.session.commit()


    """更新数据"""
    # # 给报读了4号课程的同学，返现红包200块钱
    # course = Course.query.get(3)
    # for student in course.student_list:
    #     student.money += 200
    # db.session.commit()


    # db.Table的缺陷: 无法通过主模型直接操作db.Table中的外键之外的其他字段，例如：无法读取购买课程的时间
    course = Course.query.get(3)
    print(course.student_list.all())

    # 解决：在声明2个模型是多对多的关联关系时，如果需要在python中操作关系表的数据，则可以把关联关系使用第三个模型来创建声明，
    # 就是不要使用db.Table创建关系表了，改成关系模型来绑定2者的关系，把模型的多对多拆分成2个1对多

    # 多对多可以拆解成3个模型（2个主模型，1个关系模型，关系模型保存了2个主模型的外键，关系表单独作为一个关系模型存在。


    return "ok"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
