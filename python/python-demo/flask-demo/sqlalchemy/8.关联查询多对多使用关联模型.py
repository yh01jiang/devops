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
    __tablename__ = "t_nvm_student_course_2"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    sid = db.Column(db.Integer, db.ForeignKey("t_nvm_student_2.id"), comment="学生ID")
    cid = db.Column(db.Integer, db.ForeignKey("t_nvm_course_2.id"), comment="课程ID")
    created_time = db.Column(db.DateTime, default=datetime.now, comment="购买时间")
    # 关联属性
    student = db.relationship("Student", uselist=False, backref=backref("to_relation", uselist=True, lazy="dynamic"))
    course = db.relationship("Course", uselist=False, backref=backref("to_relation", uselist=True, lazy="dynamic"))


class Student(db.Model):
    """学生信息模型"""
    __tablename__ = "t_nvm_student_2"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"


class Course(db.Model):
    """课程信息模型"""
    __tablename__ = "t_nvm_course_2"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="课程")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"

@app.route("/")
def index():
    """添加数据"""
    student = Student(
        name="xiaozhao",
        age=13,
        sex=False,
        to_relation=[
            StudentCourse(course=Course(name="python入门")),
            StudentCourse(course=Course(name="python初级")),
            StudentCourse(course=Course(name="python进阶")),
        ]
    )
    db.session.add(student)
    db.session.commit()

    """在已有课程的基础上，新增学生报读课程。"""
    student = Student(
        name="xiaohong",
        age=14,
        sex=False,
        money=30000,
    )
    db.session.add(student)
    db.session.commit()
    
    student = Student.query.filter(Student.name == "xiaohong").first()
    student.to_relation.extend([
        StudentCourse(
            course=Course.query.get(1)  # 已经存在的课程，给学生报读
        ),
        StudentCourse(
            course=Course(name="python高级")  # 新增课程，并让当前学生报读该课程
        )
    ])
    db.session.commit()



    # 已有学生和课程，对学生购买课程进行记录

    student1 = Student.query.get(2)
    course_list = Course.query.filter(Course.id.in_([2,3])).all()
    student1.to_relation.extend([StudentCourse(course=course) for course in course_list])
    db.session.commit()

    """查询操作"""
    # 查询学生购买的课程
    student = Student.query.get(1)
    print([relation.course for relation in student.to_relation])

    #查看指定课程有哪些学生购买了
    course = Course.query.get(1)
    print([relation.student for relation in course.to_relation])

    # 查询2号学生购买的每个课程的时间
    student = Student.query.get(2)
    for relation in student.to_relation:
        print(relation.course.name, relation.created_time)

    """更新数据"""
    # 给购买了2号课程的学生返现
    course = Course.query.get(2)
    for relation in course.to_relation:
        relation.student.money += 200
    db.session.commit()
    return "ok"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)