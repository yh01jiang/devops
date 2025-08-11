import socket


client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # 流式协议===》tcp协议

while True:
    msg=input("输入要发送的消息>>>: ").strip()
    client.sendto(msg.encode('utf-8'), ('127.0.0.1', 8085))
    # data,server_addr=client.recvfrom(1024)
    # print(data.decode('utf-8'))
    res=client.recvfrom(1024)
    print(res)



client.close()
