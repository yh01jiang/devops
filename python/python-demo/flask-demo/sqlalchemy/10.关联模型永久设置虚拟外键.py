from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)
# 连接数据库url（python3环境）
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456789@127.0.0.1:3306/school?charset=utf8"
# 动态追踪对象修改并且发送信号，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 查询时会显示原始sql语句
app.config["SQLALCHEMY_ECHO"] = True

# 把SQLAlchemy组件注册到项目中
db = SQLAlchemy()
db.init_app(app)


class StudentCourse(db.Model):
    __tablename__ = "t_virtual_foregin_key_student_course_2"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    student_id = db.Column(db.Integer, index=True, comment="学生ID")
    course_id = db.Column(db.Integer, index=True, comment="课程ID")
    created_time = db.Column(db.DateTime, default=datetime.now, comment="购买时间")
    # 只需要根据关联属性来设置[比原来设置物理外键，多出2个属性设置：primaryjoin与foreign_keys]
    # primary join：明确指定两个模型之间使用的连表条件
    # foreign_keys : 在这里代表的 是虚拟外键

    student= db.relationship("Student", uselist=False,backref=backref("to_relation", uselist=True,lazy="dynamic"), 
        primaryjoin="Student.id==StudentCourse.student_id",
        foreign_keys="StudentCourse.student_id"
        )
    course = db.relationship("Course", uselist=False, backref=backref("to_relation", uselist=True, lazy="dynamic"),
        primaryjoin="Course.id==StudentCourse.course_id",
        foreign_keys="StudentCourse.course_id"
    )


class Student(db.Model):
    """学生信息模型"""
    __tablename__ = "t_virtual_foregin_key_student_2"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"


class Course(db.Model):
    """课程信息模型"""
    __tablename__ = "t_virtual_foregin_key_course_2"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="课程")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"

@app.route("/")
def index():
    """分别给不同的模型添加测试数据"""
    # stu0 = Student(name="xiaozhao", age=15, sex=True, money=1000)
    # stu1 = Student(name="xiaoming", age=16, sex=True, money=1000)
    # stu2 = Student(name="xiaobai", age=18, sex=False, money=1000)
    # stu3 = Student(name="xiaohei", age=21, sex=True, money=1000)
    # stu4 = Student(name="xiaolan", age=18, sex=False, money=1000)
    # db.session.add_all([stu0, stu1, stu2, stu3, stu4])
    
    # course1 = Course(name="python基础")
    # course2 = Course(name="python入门")
    # course3 = Course(name="python进阶")
    # course4 = Course(name="python高级")
    # course5 = Course(name="python实战")
    # db.session.add_all([course1, course2, course3, course4, course5])
    
    # # 学生购买课程
    # data = [
    #     StudentCourse(student_id=1,course_id=1),
    #     StudentCourse(student_id=1,course_id=2),
    #     StudentCourse(student_id=1,course_id=3),
    #     StudentCourse(student_id=2,course_id=1),
    #     StudentCourse(student_id=2,course_id=2),
    #     StudentCourse(student_id=3,course_id=3),
    #     StudentCourse(student_id=3,course_id=4),
    #     StudentCourse(student_id=4,course_id=1),
    #     StudentCourse(student_id=4,course_id=2),
    #     StudentCourse(student_id=4,course_id=5),
    #     StudentCourse(student_id=5,course_id=1),
    #     StudentCourse(student_id=5,course_id=2),
    #     StudentCourse(student_id=5,course_id=3),
    #     StudentCourse(student_id=5,course_id=4),
    # ]
    # db.session.add_all(data)
    # db.session.commit()


    """查询3号学生购买了哪些课程？"""
    student = Student.query.get(3)
    print([{"id":relation.course.id, "name": relation.course.name} for relation in student.to_relation.all()])

    """查询5个课程都有哪些学生购买了?"""
    course = Course.query.get(5)
    print([{"id":relation.student.id, "name": relation.student.name} for relation in course.to_relation.all()])
  


    return "ok"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)