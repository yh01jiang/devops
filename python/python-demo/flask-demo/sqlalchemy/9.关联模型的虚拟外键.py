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
    __tablename__ = "t_virtual_foregin_key_student_course"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    student_id = db.Column(db.Integer, index=True, comment="学生ID")
    course_id = db.Column(db.Integer, index=True, comment="课程ID")
    created_time = db.Column(db.DateTime, default=datetime.now, comment="购买时间")
    # 只需要根据关联属性来设置


class Student(db.Model):
    """学生信息模型"""
    __tablename__ = "t_virtual_foregin_key_student"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"


class Course(db.Model):
    """课程信息模型"""
    __tablename__ = "t_virtual_foregin_key_course"
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
    # 方法1. 手动基于代码进行关联查询
    student_course_list = StudentCourse.query.filter(StudentCourse.student_id==3).all()
    course_id_list = [relation.course_id for relation in student_course_list]
    course_list = Course.query.filter(Course.id.in_(course_id_list)).all()
    print(course_list)

    # 方法2. 基于临时逻辑外键来关联查询
    # 主模型.query.join(从模型类名, 关系语句)
    # 主模型.query.join(从模型类名, 主模型.主键==从模型类名.外键)
    # with_entities： 代表查哪些字段


    # 两个模型的临时逻辑外键关联
    data = Student.query.join(
        StudentCourse, Student.id == StudentCourse.student_id
    ).with_entities(StudentCourse.course_id).filter(Student.id==3).all()
    print(data)


    # 两个以上模型的临时逻辑外键关联
    data = Student.query.join(
        StudentCourse, Student.id == StudentCourse.student_id
    ).join(
        Course, StudentCourse.course_id == Course.id
    ).with_entities(
        StudentCourse.course_id, Course.name
    ).filter(Student.id==3).all()

    print(data)


    return "ok"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

