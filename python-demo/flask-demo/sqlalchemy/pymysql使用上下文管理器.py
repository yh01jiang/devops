import pymysql

# 建立数据库连接
with pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="123456789",
    database="school",
    port=3306
) as connection:
    # 创建游标对象
    with connection.cursor() as cursor:
        # 执行SQL查询
        cursor.execute("SELECT * FROM student")

        # 获取查询结果
        result = cursor.fetchall()

        # 处理结果
        for row in result:
            print(row)