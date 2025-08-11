import db
from datetime import datetime

# 1. 创建一个与数据库对应的模型类对象
class Student(db.Model):
    """学生表模型"""
    __tablename__ = "tb1_student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    sex = db.Column(db.Boolean, default=True)
    age = db.Column(db.SmallInteger)
    classes = db.Column("class", db.SMALLINT)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=1)
    addtime = db.Column(db.DateTime, default=datetime.now)
    orders = db.Column(db.SMALLINT, default=1)

    def __repr__(self):
        """
        当实例对象被使用print打印时，自动执行此处当前，
        当前__repr__使用与上面__str__一致，返回值必须时字符串格式，否则报错！！！
        """
        return f"<{self.__class__.__name__} {self.name}>"
    
    def todict(self):
        return {
            "id": self.id,
            "name": self.name
        }


if __name__ == '__main__':
    db.Model.metadata.create_all(db.engine)
    """ 1.添加一条数据 """
    student = Student(name="小明1号", classes="305", sex=True, age=18, description="滚出去..")
    db.session.add(student)  # 相当于 pymysql的execute
    db.session.commit()      # 想当于事物提交

    # """ 2.添加多条数据 """
    student1 = Student(name="小明1号", classes="305", sex=True, age=18, description="滚出去..")
    student2 = Student(name="小明2号", classes="306", sex=False, age=19, description="滚出去..")
    student3 = Student(name="小明3号", classes="307", sex=True, age=20, description="滚出去..")
    student4 = Student(name="小明4号", classes="308", sex=False, age=21, description="滚出去..")
    db.session.add_all([student1, student2, student3, student4])
    db.session.commit()


    """ 3.查询一条数据 """

    """
    get 用于根据主键值获取一条，如果查不到数据，则返回None，查到结果则会被ORM底层使用当前模型类来进行实例化成模型对象
    get 可以接收1个或多个主键参数，只能作为主键值
    """
    # get(4) 相当于 where id=4;
    student = db.session.query(Student).get(4)  # 如果查询的是联合主键 写法： get((5,10)) 或 get({"id": 5, "version_id": 10})
    print(student, type(student))
    # <__main__.Student object at 0x7f4161c69520> <class '__main__.Student'>


    """
    使用first获取查询结果集的第一个结果
    first 不能接收任何参数，所以一般配合filter或者filter_by 来进行使用的
    """
    student = db.session.query(Student).first()

    # 获取属性值
    if student:
        print(f"id={student.id}, name={student.name}, age={student.age}")


    """ 4.查询多条数据 """
    student_list = db.session.query(Student).all()
    print(student_list)

    # 基于循环输出每一个模型对象中的属性
    for student in student_list:
        print(f"id={student.id}, name={student.name}, classes={student.classes}")

    """ 5.过滤条件查询 """
    """
    filter_by - 精确查询
    filter_by支持值相等=号操作，不能使用大于、小于或不等于的操作一律不能使用
    """
    # 单个字段条件
    students = db.session.query(Student).filter_by(name="小明1号").all()
    print(students)

    # 多个and条件
    students = db.session.query(Student).filter_by(sex=1, age=18).all()
    print(students)

    """
    filter - 匹配查询
    支持所有的运算符表达式，比filter精确查询要更强大
    注意：条件表达式中的字段名必须写上模型类名
    filter中的判断相等必须使用==2个等号
    """
    # 获取查询结果集的所有数据，列表
    students = db.session.query(Student).filter(Student.age > 17).all()
    print(students) # [<Student 小明1号>, <Student 小明1号>, <Student 小明3号>, <Student 小明4号>]
    
    # 获取查询结果集的第一条数据，模型对象
    students = db.session.query(Student).filter(Student.age < 18).first()
    print(students) # <Student 小明1号>

    """in运算符"""
    students = db.session.query(Student).filter(Student.id.in_([1, 3, 4])).all()
    print(students) # [<Student 小明1号>, <Student 小明1号>, <Student 小明2号>]

    """多条件表达式"""
    """多个or条件"""
    from sqlalchemy import or_
    # 查询302或303班的学生
    students = db.session.query(Student).filter(or_(Student.classes==303, Student.classes==302)).all()
    print(students) # [<Student 小明1号>, <Student 小明2号>]

    """多个and条件"""
    students = db.session.query(Student).filter(Student.age==18, Student.sex==1).all()
    print(students) # [<Student 小明1号>, <Student 小明3号>]

    from sqlalchemy import and_
    students = db.session.query(Student).filter(and_(Student.age == 18, Student.sex == 1)).all()
    print(students) # [<Student 小明1号>, <Student 小明3号>]

    """and_主要用于与or_一起使用的"""
    #查询305的18岁男生 或者 305班的17岁女生
    from sqlalchemy import and_, or_
    students = db.session.query(Student).filter(
        or_(
            and_(Student.classes==305, Student.age==18, Student.sex==1),
            and_(Student.classes==305, Student.age==17, Student.sex==2),
        )
    ).all()

    students = db.session.query(Student).filter(
        and_(
            Student.classes == 305,
            or_(
                and_(Student.age == 18, Student.sex == 1),
                and_(Student.age == 17, Student.sex == 2)
            )
        )
    ).all()

    print(students) # [<Student 小明1号>, <Student 小明4号>]


    """更改数据"""
    # 查询要更改的数据[目的为了让ORM实现表记录与模型对象的映射]

    student_list = db.session.query(Student).all()
    print([student.todict() for student in student_list])  # 获取模型对象中所有数据

    student = db.session.query(Student).get(1)
    print(student, student.id, student.name)
    print(dir(student))
    student.age = 16
    student.classes = 301
    db.session.commit()

    """删除数据"""
    # 查询要删除的数据[目的为了让ORM实现表记录与模型对象的映射]
    student = db.session.query(Student).get(6)
    db.session.delete(student)
    db.session.commit()

    """限制结果数量"""
    student_list = db.session.query(Student).limit(3).all()
    print(student_list)

    """结果排序"""
    student_list = db.session.query(Student).order_by(Student.classes.asc(), Student.age.desc()).all()
    print([student.todict() for student in student_list])

    # 事务操作
    db.session.begin()
    db.session.commit()
    db.session.rollback()



    """DQL-读取数据"""
    # 返回游标对象
    cursor = db.session.execute("select * from tb_student")
    # # 获取一条结果,mappings方法表示把结果从元组转换成字典
    student = cursor.mappings().fetchone()
    print(student)

    # 获取指定数量结果
    student_list = cursor.mappings().fetchmany(2)
    print(student_list)

    # 获取所有结果
    student_list = cursor.mappings().fetchall()
    print(student_list)


    """DML-写入数据"""
    sql = "insert into tb_student(name, class, age, sex, description) values(:name, :class, :age, :sex, :description)"
    data = {
        "class": "305",
        "age": 19,
        "name": "xiaohong",
        "sex": 0,
        "description": ".....",
    }

    cursor = db.session.execute(sql, params=data)
    db.session.commit()
    print(cursor.lastrowid)  # 获取最后添加的主键ID


    # student = db.session.query(Student).get(1)
    # 不仅会返回当前模型的字段属性，
    # 还会返回当前对象与数据表的映射关系
    # 如果有使用了外键，还会记录表与表之间的关联关系
    # print(student.__dict__)



    