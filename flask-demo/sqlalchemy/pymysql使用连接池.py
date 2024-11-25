from dbutils.pooled_db import PooledDB
import pymysql

# 第一种方式
host = 'localhost'  # 数据库主机地址
port =3306  # 数据库的端口号
user = 'root' # 数据库登录用户名
password = '123456789' # 对应的登录密码
database = 'school' # 需要连接的数据库名称
charset = 'utf8'  # 数据库字符集（编码）


# 配置连接池
pool = PooledDB(
    creator=pymysql,  # 使用pymysql库创建连接
    maxconnections=5,  # 连接池允许的最大连接数
    mincached=2,  # 初始化时连接池中至少创建的空闲的连接，0表示不创建
    maxcached=5,  # 连接池中最多闲置的连接，0和None表示不限制
    maxshared=3,  # 连接池中最多共享的连接数量，0和None表示全部共享
    blocking=True,  # 当连接池达到最大数量时，是否阻塞等待连接释放
    maxusage=None,  # 单个连接最多被重复使用的次数，None表示无限制
    setsession=[],  # 设置开始会话前执行的命令列表
    ping=0,         # 设置ping服务器端的选项，作用是检查是否服务器端可用
    host=host,
    port=port,
    user=user,
    password=password,
    database=database,
    charset=charset

    # 第二种方式
    # host="127.0.0.1",
    # user="root",
    # password="123456789",
    # database="school",
    # port=3306,
    # charset='utf8'


)

# 从连接池获取连接
connection = pool.connection()

# 使用连接进行操作
cursor = connection.cursor()
cursor.execute("SELECT * FROM student")
result = cursor.fetchall()
for row in result:
    print(row)

# 关闭游标和连接
cursor.close()
connection.close()