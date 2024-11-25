
# 服务端应满足的特点：
# 1. 一直提供服务
# 2. 并发的提供服务
import socket

# 1. 买手机 
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # 流式协议===》tcp协议

# 2. 绑定手机卡
server.bind(('127.0.0.1', 8085))  # 端口0-65535 1024之前为系统所用

# 3. 开机
server.listen(5)  # 5指的是半链接池的大小
print('服务端启动完成,监听地址为: %s:%s' %('127.0.0.1', 8085))

# 加上链接循环
while True:
    # 4. 等待电话连接请求
    conn, client_addr=server.accept()  # 解压赋值
    print(conn)  # 套接字对象
    print("客户端的ip和端口: " ,client_addr)


    # 5. 收\发消息
    while True:
        try:
            data=conn.recv(1024)  # 最大接收的数据量是1024bytes，收到的是bytes类型
            if len(data) == 0:
                # 在unix系统下，如果data收到的是空，意味这是一种异常的行为：客户端非法断开。
                break   # 如果不加，那么正在链接的客户端突然断开，recv便不再阻塞，死循环发生。
            print("客户端发来的消息： ", data.decode('utf-8'))
            conn.send(data.upper())
        except Exception:
            # 针对于windows 系统
            break


    # 6.关闭电话连接
    conn.close()

# 7. 关机（可选操作）
server.close()