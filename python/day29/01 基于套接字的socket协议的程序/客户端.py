import socket

# 1. 买手机 
# socket.socket()  # socket模块中有个socket类，加() 实例化成一个对象
# # 有一个参数 type=SOCK_STREAM，即不传参数，默认就是TCP协议
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # 流式协议===》tcp协议

# 2. 拨通服务端电话
client.connect(('127.0.0.1', 8085))

# 3. 通信
# import time
# time.sleep(10)
client.send('hello 哈哈哈'.encode('utf-8'))
data=client.recv(1024)
print(data.decode('utf-8'))


# 4. 关闭连接（必选的操作）
client.close()



# 客户端的输出：
# HELLO 哈哈哈