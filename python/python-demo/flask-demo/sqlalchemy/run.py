# import pymysql

#1.导入
from sqlalchemy import create_engine  # 驱动引擎

#2.创建引擎
engine = create_engine(
	    "mysql+pymysql://root:123456789@127.0.0.1:3306/school?charset=utf8mb4",
	    max_overflow=0,  # 超过连接池大小外最多创建的连接
	    pool_size=5,     # 连接池大小
	    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
	    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
	)


# 3. 使用引擎拿到链接

engine.execute('create table if not EXISTS t1(id int PRIMARY KEY auto_increment,name char(32));')
# cur=engine.execute('insert into t1 values(%s,%s);',[(1,"egon1"),(2,"egon2"),(3,"egon3")]) #按位置传值

# cur=engine.execute('insert into t1 values(%(id)s,%(name)s);',name='egon4',id=4) #按关键字传值

#4 新插入行的自增id
# print(cur.lastrowid)



#5 查询
cur=engine.execute('select * from t1')

cur.fetchone() #获取一行
cur.fetchmany(2) #获取多行
cur.fetchall() #获取所有行