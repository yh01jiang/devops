from sqlalchemy import create_engine  # 驱动引擎
from sqlalchemy.ext.declarative import declarative_base  # 数据库基类
from sqlalchemy import *
from sqlalchemy import Column,Integer,String,DateTime,Enum,ForeignKey,UniqueConstraint,ForeignKeyConstraint,Index,Boolean
from sqlalchemy.orm import sessionmaker  # 连接会话
engine=create_engine('mysql+pymysql://root:123456789@127.0.0.1:3306/school?charset=utf8',max_overflow=5,echo=True)

# 模型类对象的基类
Base=declarative_base()

# 创建数据库连接
DbSession = sessionmaker(bind=engine)
session = DbSession()

# 创建数据基类
Base = declarative_base()


# 创建表模型
class User(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    age = Column(Integer)
    sex = Column(Boolean)
    # 因为class在python是类，所以此处使用映射处理
    class_name = Column("class",String(255))

    # 类可以通过定义 __repr__() 方法来控制此函数为它的实例所返回的内容。
    # 添加 __repr__() 方法，返回一个自定义的字符串即可
    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"



if __name__ == '__main__':
    # 如果没有提前声明模型中的数据表，则可以采用以下代码生成数据表结构
    # 如果数据库中已经声明了有数据表，则不会继续生成。
    Base.metadata.create_all(engine)


    # 获取模型对应的所有数据
    data_list = session.query(User).all()
    print(data_list)

    # 循环输出
    for data in data_list:
        print(data, data.id, data.name, data.age)


    # 获取一条数据（参数为主键，如果查询不到，则返回结果为None）

    student1 = session.query(User).get(500)
    if student1:
        print(student1,student1.name, student1.age,student1.class_name,student1.sex)

    else:
        print("查无此人")

    # 按条件查询
    student_list = session.query(User).filter(User.sex==True, User.class_name=='304',).all()
    #print(student_list)
    """filter支持> < 的，filter_by 不支持"""
    stu_list = session.query(User).filter(User.sex==True, User.class_name >'304',).all()
    print(stu_list)

    # 添加一条数据
    user = User(
        name="张三丰",
        age = 18,
        sex = True,
        class_name = "305"
    )

    session.add(user)
    session.commit()

    # 修改操作
    student = session.query(User).filter_by(name="张三丰").first()
    if student:
        student.name = "张四风"
        student.age= 21
        session.commit()

    # 删除一条数据操作
    data1 = session.query(User).filter_by(name="张四风").first()
    session.delete(data1)
    session.commit()

    # 添加多条数据
    student_list = [
        User(name="xiaohei", age=22, sex=True, class_name=304),
        User(name="xiaohuang", age=18, sex=True, class_name=304),
        User(name="xiaobai", age=18, sex=True, class_name=873)

    ]

    session.add_all(student_list)
    session.commit()

    # 更新多条数据
    session.query(User).filter(User.name=="xiaobai").update({User.class_name: User.class_name+1})
    session.commit()


    # 删除多条数据
    session.query(User).filter(User.id>21).delete()
    session.commit()

    """原生SQL语句"""
    cursor = session.execute("select * from student")
    """ 1条数据 """
    data = cursor.fetchone()
    print(data)

    """" 所有数据 """
    data2 = cursor.fetchall()
    print(data2)

    # 写操作
    cursor = session.execute(
        'insert into student(name, age, sex, class) values(:name, :age, :sex, :class)',
        params = {
            "name": "xiaoliu",
            "age": 19,
            "sex": 0,
            "class": "307",

        })

    session.commit()
    print(cursor.lastrowid)