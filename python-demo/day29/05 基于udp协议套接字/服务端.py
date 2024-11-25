import socket

server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # 数据报协议===》udp协议


# udp协议不建立链接，所以不需要服务器的监听和接收连接。
server.bind(('127.0.0.1', 8085))  # 端口0-65535 1024之前为系统所用



# recvfrom()表示从套接字读取消息
# sendto()很好理解，就是发送消息给别人。参数1表示消息内容，参数2就是发送到哪里（也就是对方的地址）
while True:
    data,client_addr=server.recvfrom(1024)
    print(data.decode('utf-8'),client_addr)
    server.sendto(data.upper(),client_addr)
    

# 6.关闭电话连接
server.close()
