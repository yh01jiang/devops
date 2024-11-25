from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text  # 字段、整型
from sqlalchemy import *


# 1. 创建数据库驱动（引擎）
engine = create_engine(
    # 连接数据库的URL
    # url="驱动名称://账户:密码@IP地址:端口/数据库名?charset=utf8mb4",  # 如果底层驱动是pymysql
    url="mysql+pymysql://root:123456789@127.0.0.1:3306/school?charset=utf8mb4",  # 如果底层驱动是pymysql
    # url="mysql://root:123@127.0.0.1:3306/students?charset=utf8mb4",  # 如果底层驱动是MySQLdb
    echo=True,  # 当设置为True时会将orm语句转化为sql语句打印，一般debug的时候可用
    pool_size=10,  # 连接池的数据库连接数量，默认为5个，设置为0时表示连接无限制
    max_overflow=30,    # 连接池的数据库连接最大数量，默认为10个
    pool_recycle=60*30  # 设置时间以限制数据库连接多久没使用则自动断开（指代max_overflow-pool_size），单位：秒
)

# 基于底层数据库驱动建立数据库连接会话，相当于cursor游标
DbSession = sessionmaker(bind=engine)
session = DbSession()
# 模型类对象的基类，内部提供了数据库的基本操作以及共同方法
Model = declarative_base()
