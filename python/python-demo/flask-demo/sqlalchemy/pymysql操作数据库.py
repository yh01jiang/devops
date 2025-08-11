""" 连接mysql数据库 """
import pymysql

# 建立数据库连接
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456789',
    database='school',
    port=3306
)

# 创建游标对象
cursor = connection.cursor()

"""
# 查询数据
# 执行sql查询
# cursor.execute("SELECT * FROM student")


# 获取查询结果
# result = cursor.fetchall()

#  处理结果
# for row in result:
#     print(row)

'''获取一条数据 
result = cursor.fetchone()
print(result)
'''

"""

""" 插入数据 
sql = "INSERT INTO student (name, age, sex, class) VALUES ('John', 25, 1, 330)"
cursor.execute(sql)
connection.commit()
"""


"""
# 更新数据
sql = "UPDATE student SET age = 26 WHERE name = 'John'"
cursor.execute(sql)
connection.commit()
"""

"""
# 删除数据
sql = "DELETE FROM student WHERE name = 'John'"
cursor.execute(sql)
connection.commit()
"""

'''
使用cursor.execute()方法来执行SQL语句，当更改表中数据时，必须调用conn.commit()方法来提交更改，否则数据库表中的数据不会发生改变。
操作完成后，可以使用cursor.fetchall()方法获取查询结果，该方法返回一个元组。


'''


# 关闭游标和连接
cursor.close()
connection.close()