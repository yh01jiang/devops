from socket import *
import struct
client=socket(AF_INET,SOCK_STREAM)
client.connect(('127.0.0.1', 8089))

while True:
    msg=input('请输入命令>>>: ').strip()
    if len(msg) == 0:
        continue
    client.send(msg.encode('utf-8'))
    # 解决粘包问题思路：
    # 一.先接收固定长度的头，解析出数据的描述信息，包括数据的总大小total_size
    total_size=***

    # 二 根据解析出的描述信息，接收真实的数据
    # 2. recv_size=0,循环接收，每接收一次，recv+=接收长度
    # 3. 直到recv_size 等于 total_size, 结束循环
    recv_size = 0
    while recv_size < total_size:
        recv_data=client.recv(1024)
        recv_size+=len(recv_data)
        print(recv_data.decode('utf-8'), end='')
    else:
        print()

    cmd_res=client.recv(1024)  # 本次最大接收为1024 bytes
    print(cmd_res.decode('utf-8'))  # 强调windows系统用gbk编码


# 粘包问题出现的原因：
    # 1. tcp是流式协议，数据像水流一样粘在一起，没有任何边界区分。
    # 2. 收数据没有收干净，有残留，就会跟下次数据混淆在一起。（收数据其实是从缓存中收数据）


# 如何解决？ 
    # 收干净点，每次都收干净，不要有任何残留。
    
    
    