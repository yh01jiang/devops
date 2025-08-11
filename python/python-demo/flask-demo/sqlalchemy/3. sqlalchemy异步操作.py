import asyncio
import async_db as db
from datetime import datetime

# 1. 创建一个与数据库对应的模型类对象
class Student(db.Model):
    """学生表模型"""
    __tablename__ = "async_student"
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
        return f"<{self.__class__.__name__} {self.name}>"

async def main():
    # 异步数据迁移
    async with db.engine.begin() as conn:
        # 删除当前程序中所有的模型对应的数据表
        # await conn.run_sync(Model.metadata.drop_all)

        # 创建当前程序中所有的模型的数据表，如果数据表不存在的情况下
        await conn.run_sync(db.Model.metadata.create_all)

    # 开启会话
    async with db.async_session() as session:
        # 开启事务
        async with session.begin():
            """DQL - 查询数据"""
            # # 拼接SQL语句
            sql = db.select(Student).filter(Student.classes == 305).order_by(Student.id)
            print(sql)
            # 异步执行SQL语句
            student = await session.execute(sql)
            # 获取一个结果
            print(student.first())
            # 获取多个结果
            print(student.mappings().all())

            """DML - 写入数据"""
            student1 = Student(name="小明1号", classes="302", sex=True, age=18, description="滚出去..")
            student2 = Student(name="小明2号", classes="303", sex=True, age=18, description="滚出去..")
            student3 = Student(name="小明3号", classes="304", sex=True, age=18, description="滚出去..")
            student4 = Student(name="小明4号", classes="305", sex=True, age=18, description="滚出去..")
            # 添加一条数据
            session.add(student1)
            # 添加多条数据
            session.add_all([student1, student2, student3,student4])

            # 异步提交事务
            await session.commit()

if __name__ == '__main__':
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())