import socket

# 1. 买手机 
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # 流式协议===》tcp协议

# 2. 绑定手机卡
server.bind(('127.0.0.1', 8085))  # 端口0-65535 1024之前为系统所用

# 3. 开机
server.listen(5)  # 5指的是半链接池的大小   半连接池，允许等待的最大个数
print('服务端启动完成,监听地址为: %s:%s' %('127.0.0.1', 8085))


# 4. 等待电话连接请求
conn, client_addr=server.accept()  # 解压赋值
# print(conn)  # 套接字对象
print("客户端的ip和端口: " ,client_addr)


# 5. 收\发消息
data=conn.recv(1024)  # 最大接收的数据量是1024bytes，收到的是bytes类型
print("客户端发来的消息： ", data.decode('utf-8'))
conn.send(data.upper())

# 6.关闭电话连接
conn.close()

# 7. 关机（可选操作）
server.close()



# 服务端输出：
# 服务端启动完成,监听地址为: 127.0.0.1:8085
# <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 8085), raddr=('127.0.0.1', 60786)>
# 客户端的ip和端口:  ('127.0.0.1', 60786)
# 客户端发来的消息：  hello 哈哈哈