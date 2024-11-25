import pymysql

# 建立数据库连接
conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="123456789",
    database="school",
    port=3306
)

# 创建游标对象
cursor = conn.cursor()

# 批量插入数据
insert_query = "INSERT INTO student (name, age, sex, class) VALUES (%s, %s, %s, %s)"
data_to_insert = [('barry', 27, 1, 555), ('elaina', 28, 0, 444), ('小吉他', 10, 0, 333)]
cursor.executemany(insert_query, data_to_insert)

# 提交事务
conn.commit()

# 关闭游标和连接
cursor.close()
conn.close()