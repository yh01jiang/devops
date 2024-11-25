import pymysql

try: 
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

    # 执行SQL查询
    cursor.execute("SELECT * FROM student")

    # 获取查询结果
    result = cursor.fetchall()

    # 打印处理结果
    for row in result:
        print(row)

except pymysql.Error as e:
    print(f"Error: {e}")

finally:
    # 关闭游标和连接
    cursor.close()
    conn.close()