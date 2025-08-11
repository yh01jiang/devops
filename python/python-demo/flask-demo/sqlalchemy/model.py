from sqlalchemy import create_engine  # 驱动引擎
from sqlalchemy.ext.declarative import declarative_base  # 数据库基类
from sqlalchemy import Column,Integer,String,DateTime,Enum,ForeignKey,UniqueConstraint,ForeignKeyConstraint,Index
from sqlalchemy.orm import sessionmaker  # 连接会话
engine=create_engine('mysql://root@127.0.0.1:3306/school?charset=utf8',max_overflow=5,echo=True)

Base=declarative_base()

# 创建数据库连接
DbSession = sessionmaker(bind=engine)
session = DbSession()

# 创建数据基类
Model = declarative_base()



# 测试入门


import sqlalchemy
print(sqlalchemy.__version__)



from sqlalchemy import create_engine


engine=create_engine('mysql://root:123456789@127.0.0.1:3306/school?charset=utf8mb4',max_overflow=5,echo=True)







