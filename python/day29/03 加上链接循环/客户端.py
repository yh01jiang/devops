import socket

# 1. 买手机 
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # 流式协议===》tcp协议

# 2. 拨通服务端电话
client.connect(('127.0.0.1', 8085))

# 3. 通信
while True:                                       # 新增通信循环，可以不断的循环，收发消息
    msg=input("输入要发送的消息>>>: ").strip()
    if len(msg) == 0:continue                     
    client.send(msg.encode('utf-8'))
    print('======>')
    data=client.recv(1024)
    print(data.decode('utf-8'))


# 4. 关闭连接（必选的操作）
client.close()



# 客户端的输出：
# HELLO 哈哈哈