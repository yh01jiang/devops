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

# 参数话查询
parametrized_query = "SELECT * FROM student WHERE name = %s AND class = %s"
query_params = ('xiaoliu', "307")
cursor.execute(parametrized_query, query_params)

# 获取查询结果
result = cursor.fetchall()

# 处理结果
for row in result:
    print(row)


# 关闭游标和连接
cursor.close()
conn.close()