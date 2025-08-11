import pymysql

# 建立数据库连接
connection = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="123456789",
    database="school",
    port=3306
)

# 创建游标对象
cursor = connection.cursor()

try:
    # 开始事务
    connection.begin()

    # 执行多个SQL语句
    cursor.execute("UPDATE student SET name = %s WHERE class = %s", ('barry123', 555))
    cursor.execute("INSERT INTO student (name, age, sex, class) VALUES (%s, %s, %s, %s)", ('muyao', 10, 0, 123))

    # 提交事务
    connection.commit()

except pymysql.Error as e:
    # 出现错误时回滚事务
    connection.rollback()
    print(f"Error: {e}")

finally:
    # 关闭游标和连接
    cursor.close()
    connection.close()